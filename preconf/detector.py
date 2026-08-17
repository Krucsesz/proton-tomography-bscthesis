import numpy as np
import opengate as gate

# Unit Shortcuts
mm = gate.g4_units.mm
um = gate.g4_units.um
cm = gate.g4_units.cm
deg = gate.g4_units.deg
mrad = gate.g4_units.mrad
eV = gate.g4_units.eV
MeV = gate.g4_units.MeV

# Gets the TOTAL energy deposited in the attached volume. If you want the deposited energy by hits, you need to set
# hc.write_to_disk = True
# and do not need the sc (DigitizerAdderActor) part.
#

# sketch
#                                                                                      z_dir            center
# World                                                                               [-w, w]             0
# phantomContainer: 300 x 300 x 300  in world no shift:                            => [-150, 150]         0
#    phantom 200 x 200 x thickness  in phantomContainer
# beam at [0, 0, -500] in world
# detectorContainer: 450 x 450 x 450 in world shifted by [0, 0, 450] (at 0 angle)  => [225, 675]          450
#    scanner_1: 270 x 164 x 100 in phantomContainer shifted by [0, 0, -175]        => [225, 325]          275
#        Tracker_Layer: [270, 164, 2.62] in scanner_1 shifted by -48.69            => [225, 227.62]       226.31
# 	       ALPIEEpi: [270, 164, 25um] in Tracker_Layer shifted by -0.9685          => [225.329, 225.354]  225.3415
#          ...
# 		   repeat with 57.8 mm shifts
#    scanner_2: 270 x 164 x 264 in detectorContainer shifted by [0, 0, 7]          => [325, 589]          457
#        Layer: [270, 164, 5.5] in scanner_2 shifted by -129.25                    => [325, 330.5]        327.75
# 	       ALPIEEpi: [270, 164, 25um] in Layer shifted by -1.6685                  => [326.069, 326.094]  326.0815
#          ...
# 		   repeat with 5.5 mm shifts


#=================#
# Detector        #
#=================#
def add_simplified_detector(sim, Container='detectorContainer', OutFile='Hits.root', particle_filter=None):
    # particle_filter: name of the particle to register, like 'proton', 'alpha', 'C12'

# --- SCANNER 1 ---
  scanner_1 = sim.add_volume('Box', 'scanner_1')
  scanner_1.mother = Container
  scanner_1.size = [270.0 * mm, 164.0 * mm, 100.0 * mm]
  scanner_1.translation = [0, 0, -175 * mm]
  scanner_1.material = 'G4_AIR'

# --- SCANNER 2 ---
  scanner_2 = sim.add_volume('Box', 'scanner_2')
  scanner_2.mother = Container
  scanner_2.size = [270.0 * mm, 164.0 * mm, 264.0 * mm]
  scanner_2.translation = [0, 0, 7 * mm]
  scanner_2.material = 'G4_AIR'

# --- TRACKER LAYER (Inside Scanner 1) ---
  tracker_layer = sim.add_volume('Box', 'TRACKER_Layer')
  tracker_layer.mother = 'scanner_1'
  tracker_layer.size = [270.0 * mm, 164.0 * mm, 2.62 * mm]
  tracker_layer.translation = [0, 0, -48.69 * mm]
  tracker_layer.material = 'G4_AIR'

# --- TRACKER COMPONENTS (Inside Tracker Layer) ---

# 1. Absorber
  absorber = sim.add_volume('Box', 'TRACKER_Absorber1')
  absorber.mother = 'TRACKER_Layer'
  absorber.size = [270.0 * mm, 164.0 * mm, 310.0 * um]
  absorber.translation = [0, 0, -1.155 * mm]
  absorber.material = 'CarbonFleece'

# 2. Glue
  glue = sim.add_volume('Box', 'TRACKER_Glue1')
  glue.mother = 'TRACKER_Layer'
  glue.size = [270.0 * mm, 164.0 * mm, 5.0 * um]
  glue.translation = [0, 0, -0.9975 * mm]
  glue.material = 'Glue'

# 3. Silicon Substrate
  sub = sim.add_volume('Box', 'TRACKER_ALPIDESub')
  sub.mother = 'TRACKER_Layer'
  sub.size = [270.0 * mm, 164.0 * mm, 14.0 * um]
  sub.translation = [0, 0, -0.988 * mm]
  sub.material = 'G4_Si' 

# 4. Silicon Epi
  epi = sim.add_volume('Box', 'TRACKER_ALPIDEEpi')
  epi.mother = 'TRACKER_Layer'
  epi.size = [270.0 * mm, 164.0 * mm, 25.0 * um]
  epi.translation = [0, 0, -0.9685 * mm]
  epi.material = 'G4_Si'

# 5. Front
  front = sim.add_volume('Box', 'TRACKER_ALPIDEFront')
  front.mother = 'TRACKER_Layer'
  front.size = [270.0 * mm, 164.0 * mm, 11.0 * um]
  front.translation = [0, 0, -0.9505 * mm]
  front.material = 'G4_Si'

# Capacitors
# 1. Al
  cap_Al = sim.add_volume('Box', 'TRACKER_CapacitorAlO')
  cap_Al.mother = 'TRACKER_Layer'
  cap_Al.size = [270.0 * mm, 164.0 * mm, 2.7 * um]
  cap_Al.translation = [0, 0, 0.70745 * mm]
  cap_Al.material = 'Al2O3' 

# 2. NiCu
  cap_NiCu = sim.add_volume('Box', 'TRACKER_CapacitorMetal')
  cap_NiCu.mother = 'TRACKER_Layer'
  cap_NiCu.size = [270.0 * mm, 164.0 * mm, 1.2 * um]
  cap_NiCu.translation = [0, 0, 0.7094 * mm]
  cap_NiCu.material = 'NiCu' 

# Cables and others
# 1. 
  cab_FDI1 = sim.add_volume('Box', 'TRACKER_CableFDI1')
  cab_FDI1.mother = 'TRACKER_Layer'
  cab_FDI1.size = [270.0 * mm, 164.0 * mm, 15.0 * um]
  cab_FDI1.translation = [0, 0, 0.7175 * mm]
  cab_FDI1.material = 'Aluminium' 

# 2. 
  cab_FDI2 = sim.add_volume('Box', 'TRACKER_CableFDI2')
  cab_FDI2.mother = 'TRACKER_Layer'
  cab_FDI2.size = [270.0 * mm, 164.0 * mm, 10.0 * um]
  cab_FDI2.translation = [0, 0, 0.73 * mm]
  cab_FDI2.material = 'Kapton' 

# 3. 
  glue2 = sim.add_volume('Box', 'TRACKER_Glue2')
  glue2.mother = 'TRACKER_Layer'
  glue2.size = [270.0 * mm, 164.0 * mm, 5.0 * um]
  glue2.translation = [0, 0, 0.7375 * mm]
  glue2.material = 'Glue' 

# 4. 
  topFDI1 = sim.add_volume('Box', 'TRACKER_TopFDI1')
  topFDI1.mother = 'TRACKER_Layer'
  topFDI1.size = [270.0 * mm, 164.0 * mm, 30.0 * um]
  topFDI1.translation = [0, 0, 0.755 * mm]
  topFDI1.material = 'Aluminium' 

# 5. 
  topFDI2 = sim.add_volume('Box', 'TRACKER_TopFDI2')
  topFDI2.mother = 'TRACKER_Layer'
  topFDI2.size = [270.0 * mm, 164.0 * mm, 20.0 * um]
  topFDI2.translation = [0, 0, 0.78 * mm]
  topFDI2.material = 'Kapton' 

# 6. 
  glue3 = sim.add_volume('Box', 'TRACKER_Glue3')
  glue3.mother = 'TRACKER_Layer'
  glue3.size = [270.0 * mm, 164.0 * mm, 5.0 * um]
  glue3.translation = [0, 0, 0.7925 * mm]
  glue3.material = 'Glue' 

# 7. 
  spacer = sim.add_volume('Box', 'TRACKER_Spacer')
  spacer.mother = 'TRACKER_Layer'
  spacer.size = [270.0 * mm, 164.0 * mm, 75.0 * um]
  spacer.translation = [0, 0, 0.8325 * mm]
  spacer.material = 'Kapton' 

# 8. 
  glue4 = sim.add_volume('Box', 'TRACKER_Glue4')
  glue4.mother = 'TRACKER_Layer'
  glue4.size = [270.0 * mm, 164.0 * mm, 5.0 * um]
  glue4.translation = [0, 0, 0.8725 * mm]
  glue4.material = 'Glue' 

# 9. 
  bottomFDI1 = sim.add_volume('Box', 'TRACKER_BottomFDI1')
  bottomFDI1.mother = 'TRACKER_Layer'
  bottomFDI1.size = [270.0 * mm, 164.0 * mm, 100.0 * um]
  bottomFDI1.translation = [0, 0, 0.925 * mm]
  bottomFDI1.material = 'Aluminium' 

# 10. 
  bottomFDI2 = sim.add_volume('Box', 'TRACKER_BottomFDI2')
  bottomFDI2.mother = 'TRACKER_Layer'
  bottomFDI2.size = [270.0 * mm, 164.0 * mm, 20.0 * um]
  bottomFDI2.translation = [0, 0, 0.985 * mm]
  bottomFDI2.material = 'Kapton' 

# 11. 
  glue5 = sim.add_volume('Box', 'TRACKER_Glue5')
  glue5.mother = 'TRACKER_Layer'
  glue5.size = [270.0 * mm, 164.0 * mm, 5.0 * um]
  glue5.translation = [0, 0, 0.9975 * mm]
  glue5.material = 'Glue' 

# 12. Absorber
  absorber2 = sim.add_volume('Box', 'TRACKER_Absorber2')
  absorber2.mother = 'TRACKER_Layer'
  absorber2.size = [270.0 * mm, 164.0 * mm, 310.0 * um]
  absorber2.translation = [0, 0, 1.155 * mm]
  absorber2.material = 'CarbonFleece'

# --- TRACKER LAYER (Inside Scanner 2) ---
  cal_layer = sim.add_volume('Box', 'Layer')
  cal_layer.mother = 'scanner_2'
  cal_layer.size = [270.0 * mm, 164.0 * mm, 5.5 * mm]
  cal_layer.translation = [0, 0, -129.25 * mm]
  cal_layer.material = 'G4_AIR'

# 1. Absorber
  cal_absorber1 = sim.add_volume('Box', 'Absorber1')
  cal_absorber1.mother = 'Layer'
  cal_absorber1.size = [270.0 * mm, 164.0 * mm, 1000.0 * um]
  cal_absorber1.translation = [0, 0, -2250 * um]
  cal_absorber1.material = 'Aluminium' 

# 2. Glue
  cal_glue = sim.add_volume('Box', 'Glue1')
  cal_glue.mother = 'Layer'
  cal_glue.size = [270.0 * mm, 164.0 * mm, 5.0 * um]
  cal_glue.translation = [0, 0, -1747.5 * um]
  cal_glue.material = 'Glue' 

# 3. Silicon Substrate
  cal_sub = sim.add_volume('Box', 'ALPIDESub')
  cal_sub.mother = 'Layer'
  cal_sub.size = [270.0 * mm, 164.0 * mm, 64.0 * um]
  cal_sub.translation = [0, 0, -1713.0 * um]
  cal_sub.material = 'G4_Si' # Using standard Geant4 Silicon

# 4. Silicon Epi
  cal_epi = sim.add_volume('Box', 'ALPIDEEpi')
  cal_epi.mother = 'Layer'
  cal_epi.size = [270.0 * mm, 164.0 * mm, 25.0 * um]
  cal_epi.translation = [0, 0, -1668.5 * um]
  cal_epi.material = 'G4_Si'

  cal_ALPIDEFront = sim.add_volume('Box', 'ALPIDEFront')
  cal_ALPIDEFront.mother = 'Layer'
  cal_ALPIDEFront.size = [270 * mm, 164 * mm, 11.0 * um]
  cal_ALPIDEFront.translation = [0, 0, -1650.5 * um]
  cal_ALPIDEFront.material = 'Silicon'

# Air Gap 

  cal_CapacitorAlO = sim.add_volume('Box', 'CapacitorAlO')
  cal_CapacitorAlO.mother = 'Layer'
  cal_CapacitorAlO.size = [270 * mm, 164 * mm, 2.7 * um]
  cal_CapacitorAlO.translation = [0, 0, -42.55 * um]
  cal_CapacitorAlO.material = 'Al2O3'

  cal_CapacitorMetal = sim.add_volume('Box', 'CapacitorMetal')
  cal_CapacitorMetal.mother = 'Layer'
  cal_CapacitorMetal.size = [270 * mm, 164 * mm, 1.2 * um]
  cal_CapacitorMetal.translation = [0, 0, -40.6 * um]
  cal_CapacitorMetal.material = 'NiCu'

  cal_CableFDI1 = sim.add_volume('Box', 'CableFDI1')
  cal_CableFDI1.mother = 'Layer'
  cal_CableFDI1.size = [270 * mm, 164 * mm, 15.0 * um]
  cal_CableFDI1.translation = [0, 0, -32.5 * um]
  cal_CableFDI1.material = 'Aluminium'

  cal_CableFDI2 = sim.add_volume('Box', 'CableFDI2')
  cal_CableFDI2.mother = 'Layer'
  cal_CableFDI2.size = [270 * mm, 164 * mm, 10.0 * um]
  cal_CableFDI2.translation = [0, 0, -20.0 * um]
  cal_CableFDI2.material = 'Kapton'

  cal_Glue2 = sim.add_volume('Box', 'Glue2')
  cal_Glue2.mother = 'Layer'
  cal_Glue2.size = [270 * mm, 164 * mm, 5.0 * um]
  cal_Glue2.translation = [0, 0, -12.5 * um]
  cal_Glue2.material = 'Glue'

  cal_TopFDI1 = sim.add_volume('Box', 'TopFDI1')
  cal_TopFDI1.mother = 'Layer'
  cal_TopFDI1.size = [270 * mm, 164 * mm, 30.0 * um]
  cal_TopFDI1.translation = [0, 0, 5.0 * um]
  cal_TopFDI1.material = 'Aluminium'

  cal_TopFDI2 = sim.add_volume('Box', 'TopFDI2')
  cal_TopFDI2.mother = 'Layer'
  cal_TopFDI2.size = [270 * mm, 164 * mm, 20.0 * um]
  cal_TopFDI2.translation = [0, 0, 30.0 * um]
  cal_TopFDI2.material = 'Kapton'

  cal_Glue3 = sim.add_volume('Box', 'Glue3')
  cal_Glue3.mother = 'Layer'
  cal_Glue3.size = [270 * mm, 164 * mm, 5.0 * um]
  cal_Glue3.translation = [0, 0, 42.5 * um]
  cal_Glue3.material = 'Glue'

  cal_Spacer2 = sim.add_volume('Box', 'Spacer2')
  cal_Spacer2.mother = 'Layer'
  cal_Spacer2.size = [270 * mm, 164 * mm, 75.0 * um]
  cal_Spacer2.translation = [0, 0, 82.5 * um]
  cal_Spacer2.material = 'Kapton'

  cal_Glue4 = sim.add_volume('Box', 'Glue4')
  cal_Glue4.mother = 'Layer'
  cal_Glue4.size = [270 * mm, 164 * mm, 5.0 * um]
  cal_Glue4.translation = [0, 0, 122.5 * um]
  cal_Glue4.material = 'Glue'

  cal_BottomFDI1 = sim.add_volume('Box', 'BottomFDI1')
  cal_BottomFDI1.mother = 'Layer'
  cal_BottomFDI1.size = [270 * mm, 164 * mm, 100.0 * um]
  cal_BottomFDI1.translation = [0, 0, 175 * um]
  cal_BottomFDI1.material = 'Aluminium'

  cal_BottomFDI2 = sim.add_volume('Box', 'BottomFDI2')
  cal_BottomFDI2.mother = 'Layer'
  cal_BottomFDI2.size = [270 * mm, 164 * mm, 20.0 * um]
  cal_BottomFDI2.translation = [0, 0, 235 * um]
  cal_BottomFDI2.material = 'Kapton'

  cal_Glue5 = sim.add_volume('Box', 'Glue5')
  cal_Glue5.mother = 'Layer'
  cal_Glue5.size = [270 * mm, 164 * mm, 5.0 * um]
  cal_Glue5.translation = [0, 0, 247.5 * um]
  cal_Glue5.material = 'Glue'

  cal_Absorber2 = sim.add_volume('Box', 'Absorber2')
  cal_Absorber2.mother = 'Layer'
  cal_Absorber2.size = [270 * mm, 164 * mm, 2500.0 * um]
  cal_Absorber2.translation = [0, 0, 1500.0 * um]
  cal_Absorber2.material = 'Aluminium'

  hc = sim.add_actor('DigitizerHitsCollectionActor', 'Hits')
  hc.attached_to = ['TRACKER_ALPIDEEpi', 'ALPIDEEpi']
  hc.output_filename = OutFile
  hc.write_to_disk = False
  hc.attributes = ['PreStepUniqueVolumeID','TotalEnergyDeposit', 'KineticEnergy', 'PostPosition',
                 'RunID', 'ThreadID', 'TrackID', 'EventID', 'ParentID', 'ParticleName', 'GlobalTime']
  hc.authorize_repeated_volumes = True
  hc.keep_zero_edep: True
  #hc.output_filename = OutFile
# fields: CurrentStepNumber Direction EventDirection EventID EventKineticEnergy EventPosition GlobalTime HitUniqueVolumeID HitUniqueVolumeIDAsInt KineticEnergy LocalTime PDGCode ParentID ParentParticleName ParticleName ParticleType Polarization Position PostDirection PostKineticEnergy PostPosition PostPositionLocal PostStepUniqueVolumeID PostStepVolumeCopyNo PreDirection PreDirectionLocal PreGlobalTime PreKineticEnergy PrePosition PrePositionLocal PreStepUniqueVolumeID PreStepVolumeCopyNo ProcessDefinedStep RunID StepLength ThreadID TimeFromBeginOfEvent TotalEnergyDeposit TrackCreatorModelIndex TrackCreatorModelName TrackCreatorProcess TrackID TrackLength TrackProperTime TrackVertexKineticEnergy TrackVertexMomentumDirection TrackVertexPosition TrackVolumeCopyNo TrackVolumeInstanceID TrackVolumeName UnscatteredPrimaryFlag Weight
  sc = sim.add_actor('DigitizerAdderActor', 'Singles')
  sc.input_digi_collection  = 'Hits'
  sc.output_filename = hc.output_filename
  sc.policy = "EnergyWeightedCentroidPosition"

  if particle_filter is not None: # like 'proton', 'alpha', 'C12'
     pass
     #f1 = gate.ParticleFilter('f_particle_detector')
     #f1.particle = particle_filter
     #sc.filters.append(f1)

  repeat_number = 2
  repeat_vector = np.array([0, 0, 57.8 * mm])
  tracker_translations = [[0, 0, -48.69 * mm] + (i * repeat_vector) for i in range(repeat_number)]
  tracker_layer.translation = tracker_translations


  repeat_number = 41
  repeat_vector = np.array([0, 0, 5.5 * mm])
  cal_translations = [[0, 0, -129.25 * mm] + (i * repeat_vector) for i in range(repeat_number)]
  cal_layer.translation = cal_translations

#  hits = sim.add_actor('PhaseSpaceActor','detector_hits')
#  hits.attached_to = ['TRACKER_ALPIDEEpi', 'ALPIDEEpi']
#  hits.output_filename = 'Detector_hits.root'
#  hits.attributes = ['PreStepUniqueVolumeID','TotalEnergyDeposit', 'KineticEnergy', 'PostPosition',
#                 'RunID', 'ThreadID', 'TrackID', 'EventID', 'ParentID', 'ParticleName', 'GlobalTime']
#  hits.authorize_repeated_volumes = True

