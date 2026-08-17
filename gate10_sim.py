import numpy as np
import opengate as gate
from scipy.spatial.transform import Rotation as R
import preconf.detector as detector
from pathlib import Path

PHANTOM = 'water'
WATER_PHANTOM_THICKNESS = 160
PHANTOM_ROTATION_ANGLE = 0
DETECTOR_ROTATION_ANGLE = 0
PRIMARY_NUMBER = 1000
#PRIMARY_NUMBER = 10000
PRIMARY_NUMBER = 100000

# beam
particle = 'proton'  # proton alpha or carbon
energy = None # override if non-default is specified

particles = {'proton': {'energy': 230.0 * gate.g4_units.MeV, 'beam': 'proton', 'filter': 'proton'},
             'alpha' : {'energy': 4 * 230.0 * gate.g4_units.MeV, 'beam': 'alpha', 'filter': 'alpha'},
             'carbon': {'energy': 12 * 430.0 * gate.g4_units.MeV, 'beam': 'ion 6 12', 'filter': 'C12'}
             }

if particle not in particles.keys():
    print(f'Unknow particle {particle}')
    exit(-1)

if energy is not None:
    particles[particle]['energy'] = energy

OutFile_pre = 'Hits'
OutPSAFile_pre = 'PSA'
OutTracker_pre = 'Hits-track'
OutCalorimeter_pre = 'Hits-calor'


# Unit Shortcuts
mm = gate.g4_units.mm
um = gate.g4_units.um
cm = gate.g4_units.cm
deg = gate.g4_units.deg
mrad = gate.g4_units.mrad
eV = gate.g4_units.eV
MeV = gate.g4_units.MeV

sim = gate.Simulation()
# sim.number_of_threads = 16
sim.physics_manager.physics_list_name = 'QGSP_BERT_EMZ'
# ionization potential
sim.physics_manager.material_ionisation_potential['G4_WATER'] = 75 * eV

#=================#
# Materials       #
#=================#
sim.volume_manager.add_material_database(str(Path(__file__).with_name('GateMaterials_v10.db')))

# Setting up this PATH variable makes it possible to load files relative to the sub-modules like phantom or detector
# /control/macroPath ./:phantoms/{PHANTOM}/:detectors/{DETECTOR}/:readouts/:visualize/:additional_material/

#=================#
# World           #
#=================#
sim.world.size = [3500 * mm, 3500 * mm, 3500 * mm]
sim.world.translation = [0, 0, 0]
sim.world.material = 'G4_AIR'
#world = sim.world

#=================#
# Phantom         #
#=================#
phantomContainer = sim.add_volume('Box', 'phantomContainer')
phantomContainer.mother = 'world'  # default
# /gate/world/daughters/systemType scanner   # No more need for it, goes to the actor definition
phantomContainer.size = [300 * mm, 300 * mm, 300 * mm]
phantomContainer.translation = [0, 0, 0]
phantomContainer.material = 'G4_AIR'
phantomContainer.rotation = R.from_euler('y', PHANTOM_ROTATION_ANGLE, degrees=True).as_matrix()  # default is radian

# /control/execute phantoms/{PHANTOM}/phantom.mac
# Water phantom
phantom = sim.add_volume('Box', 'phantom')
phantom.mother = 'phantomContainer'
phantom.size = [200 * mm, 200 * mm, WATER_PHANTOM_THICKNESS * mm]
phantom.translation = [0, 0, 0]
phantom.material = 'G4_WATER'

#=================#
# Source          #
#=================#
pbs = sim.add_source('IonPencilBeamSource', 'PBS')
pbs.particle = particle
pbs.energy.mono = particles[particle]['energy']
pbs.energy.sigma_gauss = 0.0
pbs.direction.partPhSp_x = [3 * mm, 2.8 * mrad, 3.0 * mm * mrad, 0]
pbs.direction.partPhSp_y = [3.0 * mm, 2.8 * mrad, 3.0 * mm * mrad, 0]
pbs.position.translation = [0 * mm, 0 * mm, -500 * mm] # mm
pbs.n = PRIMARY_NUMBER

#=================#
# Detector        #
#=================#
detectorContainer = sim.add_volume('Box', 'detectorContainer')
# The size and position are chosen so that the front plane is at 225 mm, which prevents overlap with phantomContainer,
# even if one of them is rotated to 45 deg: sqrt(2)*150 = 212.13 < 225.
detectorContainer.size = [450 * mm, 450 * mm, 450 * mm]
rad_from_deg = np.deg2rad(DETECTOR_ROTATION_ANGLE)
detectorContainer.translation = [450 * mm * np.sin(rad_from_deg), 0, 450 * mm * np.cos(rad_from_deg)]  # GATE 9: setThetaOfTranslation {DETECTOR_ROTATION_ANGLE} deg 
detectorContainer.material = 'G4_AIR'
detectorContainer.rotation = R.from_euler('y', DETECTOR_ROTATION_ANGLE, degrees=True).as_matrix()  # default is radian

detector.add_simplified_detector(sim,Container='detectorContainer',OutFile = f'{OutFile_pre}-{particle}.root', particle_filter=particles[particle]['filter'])

#==================================#
# Readout from overlapping volumes #
#==================================#
Z_list = np.arange(- WATER_PHANTOM_THICKNESS// 2, WATER_PHANTOM_THICKNESS // 2 + 1, 1)
pre_list = np.arange(-450, - WATER_PHANTOM_THICKNESS// 2, 25)
post_list = np.arange(WATER_PHANTOM_THICKNESS// 2 + 1, 200, 5)
Z_list = np.unique(np.concatenate((pre_list, Z_list, post_list)))
#print(f'{len(Z_list)=}')
#print('Z_list = ',Z_list)

#sim.add_parallel_world("readout_world")
#slice = sim.add_volume('Box', 'slice')
#slice.mother = 'readout_world'
#slice.size = [200 * mm, 200 * mm, 1 * mm]
#slice.translation = [[0, 0, z] for z in Z_list]

# check Actors: should be the same as Hits.root
sim.add_parallel_world("readout_world")
slice = sim.add_volume('Box', 'slice')
slice.mother = 'readout_world'
slice.size = [200 * mm, 200 * mm, 25 * um]
# track_list = [225.329*mm + i * 57.8 * mm for i in range(2)]
# calor_list = [326.069*mm + i * 5.5 * mm for i in range(41)]
# Z_list = np.concatenate((track_list, calor_list))
#Z_list =  np.arange(- WATER_PHANTOM_THICKNESS// 2, WATER_PHANTOM_THICKNESS // 2 + 1, 1)
slice.translation = [[0, 0, z] for z in Z_list]

#psa_hc = sim.add_actor('DigitizerHitsCollectionActor', 'PSA_Hits')
#psa_hc.attached_to = 'slice'
#psa_hc.output_filename = None
#psa_hc.attributes = ['PreStepUniqueVolumeID','TotalEnergyDeposit', 'KineticEnergy', 'PostPosition',
#                     'RunID', 'ThreadID', 'TrackID', 'EventID', 'ParentID', 'ParticleName', 'GlobalTime']
#psa_hc.authorize_repeated_volumes = True
#psa = sim.add_actor('DigitizerAdderActor', 'PSA')
#psa.input_digi_collection  = 'PSA_Hits'
#psa.policy = "EnergyWeightedCentroidPosition"
##psa = sim.add_actor('PhaseSpaceActor', 'PSA')
#psa.attributes = ['TotalEnergyDeposit', 'KineticEnergy', 'PostPosition',
#                 'PreStepUniqueVolumeID', 'RunID', 'ThreadID', 'TrackID', 'EventID', 'ParentID', 'ParticleName']
#psa.authorize_repeated_volumes = True
#psa.output_filename = OutPSAFile

psa = sim.add_actor('PhaseSpaceActor','PSA')
psa.attached_to = 'slice'
psa.attributes = ['TotalEnergyDeposit', 'KineticEnergy', 'PostPosition',
                  'PreStepUniqueVolumeID', 'RunID', 'ThreadID', 'TrackID', 'EventID', 'ParentID', 'ParticleName']
psa.output_filename = f'{OutPSAFile_pre}-{particle}.root'

#f1 = gate.ParticleFilter('f_particle')
#f1.particle = particles[particle]['filter']
# f1 = sim.add_filter('ParticleFilter', 'primary_filter')
# f1.user_info.parent_id = 0
#psa.filters.append(f1)

hits_track = sim.add_actor('PhaseSpaceActor','detector_hits_track')
hits_track.attached_to = 'TRACKER_ALPIDEEpi'
hits_track.output_filename = f'{OutTracker_pre}-{particle}.root'
hits_track.attributes = ['PreStepUniqueVolumeID','TotalEnergyDeposit', 'KineticEnergy', 'PostPosition',
                 'RunID', 'ThreadID', 'TrackID', 'EventID', 'ParentID', 'ParticleName', 'GlobalTime']
hits_track.authorize_repeated_volumes = True
#hits_track.filters.append(f1)

hits_calor = sim.add_actor('PhaseSpaceActor','detector_hits_calor')
hits_calor.attached_to = 'ALPIDEEpi'
hits_calor.output_filename = f'{OutCalorimeter_pre}-{particle}.root'
hits_calor.attributes = ['PreStepUniqueVolumeID','TotalEnergyDeposit', 'KineticEnergy', 'PostPosition',
                 'RunID', 'ThreadID', 'TrackID', 'EventID', 'ParentID', 'ParticleName', 'GlobalTime']
hits_calor.authorize_repeated_volumes = True
#hits_calor.filters.append(f1)

sim.random_seed = 'auto'
sim.run()
