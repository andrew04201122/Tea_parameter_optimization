# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.2.0

# ----------------------------------------------
#import ScriptEnv
#ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
import time
import os

def Simulation(Box_X, Box_Y, Box_Z, Waveport1_angle, Waveport1_position, Waveport2_angle, Waveport2_position, Waveport1_x, Waveport1_y, Waveport2_x, Waveport2_y, Iteration, frequency, Waveport1_phase, Waveport2_phase):

	BASE_HEIGHT = 10
	CASING_THICKENSS = 1
	MARGIN = 40
	GRID_SIZE = 20

	box_x_outside = Box_X
	box_y_outside = Box_Y
	box_z_outside = Box_Z

	box_x_inside = box_x_outside - CASING_THICKENSS*2
	box_y_inside = box_y_outside - CASING_THICKENSS*2
	box_z_inside = box_z_outside - BASE_HEIGHT - CASING_THICKENSS

	grid_x_start = MARGIN
	grid_y_start = MARGIN
	grid_z_start = box_z_outside/2
	grid_x_end = box_x_outside - MARGIN
	grid_y_end = box_y_outside - MARGIN
	grid_z_end = box_z_outside/2

	def set_waveport_paramter(angle, position, waveport_x, waveport_y):
		hole_x_pos, hole_y_pos, hole_z_pos, hole_x_size, hole_y_size, hole_z_size, plane_x_pos, plane_y_pos, plane_z_pos, plane_axis, waveport_width, waveport_height = 0,0,0,0,0,0,0,0,0,0,0,0
		if angle == 90:
			waveport_width = 86
			waveport_height = 43
		elif angle == 0:
			waveport_width = 43
			waveport_height = 86

		if position == "up":
			hole_x_pos = box_x_outside/2 - waveport_width/2 + waveport_x
			hole_y_pos = box_y_outside/2 - waveport_height/2 + waveport_y
			hole_z_pos = box_z_outside - CASING_THICKENSS
			hole_x_size = waveport_width
			hole_y_size = waveport_height
			hole_z_size = CASING_THICKENSS
			plane_x_pos = hole_x_pos
			plane_y_pos = hole_y_pos
			plane_z_pos = hole_z_pos + CASING_THICKENSS
			plane_axis = "Z"

		elif position == "back":
			hole_x_pos = 0
			hole_y_pos = box_y_outside/2 - waveport_width/2  + waveport_x
			hole_z_pos = box_z_outside/2 - waveport_height/2  + waveport_y
			hole_x_size = CASING_THICKENSS
			hole_y_size = waveport_width
			hole_z_size = waveport_height
			plane_x_pos = hole_x_pos
			plane_y_pos = hole_y_pos
			plane_z_pos = hole_z_pos
			plane_axis = "X"

		elif position == "front":
			hole_x_pos = box_x_outside - CASING_THICKENSS
			hole_y_pos = box_y_outside/2 - waveport_width/2 + waveport_x
			hole_z_pos = box_z_outside/2 - waveport_height/2 + waveport_y
			hole_x_size = CASING_THICKENSS
			hole_y_size = waveport_width
			hole_z_size = waveport_height
			plane_x_pos = hole_x_pos + CASING_THICKENSS
			plane_y_pos = hole_y_pos
			plane_z_pos = hole_z_pos
			plane_axis = "X"

		elif position == "right":
			hole_x_pos = box_x_outside/2 - waveport_width/2 + waveport_x
			hole_y_pos = 0
			hole_z_pos = box_z_outside/2 - waveport_height/2 + waveport_y
			hole_x_size = waveport_width
			hole_y_size = CASING_THICKENSS
			hole_z_size = waveport_height
			plane_x_pos = hole_x_pos
			plane_y_pos = hole_y_pos
			plane_z_pos = hole_z_pos
			plane_axis = "Y"
			waveport_width , waveport_height = waveport_height, waveport_width

		elif position == "left":
			hole_x_pos = box_x_outside/2 - waveport_width/2 + waveport_x
			hole_y_pos = box_y_outside - CASING_THICKENSS
			hole_z_pos = box_z_outside/2 - waveport_height/2 + waveport_y
			hole_x_size = waveport_width
			hole_y_size = CASING_THICKENSS
			hole_z_size = waveport_height
			plane_x_pos = hole_x_pos
			plane_y_pos = hole_y_pos + CASING_THICKENSS
			plane_z_pos = hole_z_pos
			plane_axis = "Y"
			waveport_width , waveport_height = waveport_height, waveport_width

		return hole_x_pos, hole_y_pos, hole_z_pos, hole_x_size, hole_y_size, hole_z_size, plane_x_pos, plane_y_pos, plane_z_pos, plane_axis, waveport_width, waveport_height


	hole1_x_pos, hole1_y_pos, hole1_z_pos, hole1_x_size, hole1_y_size, hole1_z_size, plane1_x_pos, plane1_y_pos, plane1_z_pos, plane1_axis, waveport1_width, waveport1_height = set_waveport_paramter(Waveport1_angle, Waveport1_position, Waveport1_x, Waveport1_y)
	hole2_x_pos, hole2_y_pos, hole2_z_pos, hole2_x_size, hole2_y_size, hole2_z_size, plane2_x_pos, plane2_y_pos, plane2_z_pos, plane2_axis, waveport2_width, waveport2_height = set_waveport_paramter(Waveport2_angle, Waveport2_position, Waveport2_x, Waveport2_y)

	# observe_plane
	observe_plane_x = 0
	observe_plane_y = 0
	observe_plane_z = box_z_outside/2
	observe_plane_width = box_x_outside
	observe_plane_height = box_y_outside

	oDesktop.RestoreWindow()
	oProject = oDesktop.NewProject("my_project")
	oProject.InsertDesign("HFSS", "HFSSDesign1", "DrivenModal", "")
	oDesign = oProject.SetActiveDesign("HFSSDesign1")
	oEditor = oDesign.SetActiveEditor("3D Modeler")

	# microwave device body
	oEditor.CreateBox(
		[
			"NAME:BoxParameters",
			"XPosition:="		, "0mm",
			"YPosition:="		, "0mm",
			"ZPosition:="		, "0mm",
			"XSize:="		, str(box_x_outside)+'mm',
			"YSize:="		, str(box_y_outside)+'mm',
			"ZSize:="		, str(box_z_outside)+'mm'
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Box1",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	# microwave device cavity
	oEditor.CreateBox(
		[
			"NAME:BoxParameters",
			"XPosition:="		, "1mm",
			"YPosition:="		, "1mm",
			"ZPosition:="		, "10mm",
			"XSize:="		, str(box_x_inside)+"mm",
			"YSize:="		, str(box_y_inside)+"mm",
			"ZSize:="		, str(box_z_inside)+"mm"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Box2",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, "Box1",
			"Tool Parts:="		, "Box2"
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, False
		])

	# Magnetron hole1
	oEditor.CreateBox(
		[
			"NAME:BoxParameters",
			"XPosition:="		, str(hole1_x_pos)+"mm",
			"YPosition:="		, str(hole1_y_pos)+"mm",
			"ZPosition:="		, str(hole1_z_pos)+"mm",
			"XSize:="		, str(hole1_x_size)+"mm",
			"YSize:="		, str(hole1_y_size)+"mm",
			"ZSize:="		, str(hole1_z_size)+"mm"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Box3",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, "Box1",
			"Tool Parts:="		, "Box3"
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, False
		])

	# Magnetron plane1
	oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, str(plane1_x_pos)+"mm",
			"YStart:="		, str(plane1_y_pos)+"mm",
			"ZStart:="		, str(plane1_z_pos)+"mm",
			"Width:="		, str(waveport1_width)+"mm",
			"Height:="		, str(waveport1_height)+"mm",
			"WhichAxis:="		, plane1_axis
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Rectangle1",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	# Magnetron hole2
	oEditor.CreateBox(
		[
			"NAME:BoxParameters",
			"XPosition:="		, str(hole2_x_pos)+"mm",
			"YPosition:="		, str(hole2_y_pos)+"mm",
			"ZPosition:="		, str(hole2_z_pos)+"mm",
			"XSize:="		, str(hole2_x_size)+"mm",
			"YSize:="		, str(hole2_y_size)+"mm",
			"ZSize:="		, str(hole2_z_size)+"mm"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Box4",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	oEditor.Subtract(
		[
			"NAME:Selections",
			"Blank Parts:="		, "Box1",
			"Tool Parts:="		, "Box4"
		], 
		[
			"NAME:SubtractParameters",
			"KeepOriginals:="	, False
		])

	# Magnetron plane2
	oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, str(plane2_x_pos)+"mm",
			"YStart:="		, str(plane2_y_pos)+"mm",
			"ZStart:="		, str(plane2_z_pos)+"mm",
			"Width:="		, str(waveport2_width)+"mm",
			"Height:="		, str(waveport2_height)+"mm",
			"WhichAxis:="		, plane2_axis
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Rectangle2",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])

	
	oEditor = oDesign.SetActiveEditor("3D Modeler")
	oEditor.ChangeProperty(
		[
			"NAME:AllTabs",
			[
				"NAME:Geometry3DAttributeTab",
				[
					"NAME:PropServers", 
					"Box1"
				],
				[
					"NAME:ChangedProps",
					[
						"NAME:Material",
						"Value:="		, "\"copper\""
					]
				]
			]
		])
	oModule = oDesign.GetModule("BoundarySetup")
	oModule.AssignWavePort(
		[
			"NAME:1",
			"Objects:="		, ["Rectangle1"],
			"NumModes:="		, 1,
			"UseLineModeAlignment:=", False,
			"DoDeembed:="		, False,
			"RenormalizeAllTerminals:=", True,
			[
				"NAME:Modes",
				[
					"NAME:Mode1",
					"ModeNum:="		, 1,
					"UseIntLine:="		, False,
					"CharImp:="		, "Zpi"
				]
			],
			"ShowReporterFilter:="	, False,
			"ReporterFilter:="	, [True],
			"UseAnalyticAlignment:=", False
		])
	oModule.AssignWavePort(
		[
			"NAME:2",
			"Objects:="		, ["Rectangle2"],
			"NumModes:="		, 1,
			"UseLineModeAlignment:=", False,
			"DoDeembed:="		, False,
			"RenormalizeAllTerminals:=", True,
			[
				"NAME:Modes",
				[
					"NAME:Mode1",
					"ModeNum:="		, 1,
					"UseIntLine:="		, False,
					"CharImp:="		, "Zpi"
				]
			],
			"ShowReporterFilter:="	, False,
			"ReporterFilter:="	, [True],
			"UseAnalyticAlignment:=", False
		])
	oEditor = oDesign.SetActiveEditor("3D Modeler")

	# observe_plane
	oEditor.CreateRectangle(
		[
			"NAME:RectangleParameters",
			"IsCovered:="		, True,
			"XStart:="		, str(observe_plane_x)+"mm",
			"YStart:="		, str(observe_plane_y)+"mm",
			"ZStart:="		, str(observe_plane_z)+"mm",
			"Width:="		, str(observe_plane_width)+"mm",
			"Height:="		, str(observe_plane_height)+"mm",
			"WhichAxis:="		, "Z"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Rectangle3",
			"Flags:="		, "",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "0mm",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	oEditor.CreateRegion(
		[
			"NAME:RegionParameters",
			"+XPaddingType:="	, "Percentage Offset",
			"+XPadding:="		, "0",
			"-XPaddingType:="	, "Percentage Offset",
			"-XPadding:="		, "0",
			"+YPaddingType:="	, "Percentage Offset",
			"+YPadding:="		, "0",
			"-YPaddingType:="	, "Percentage Offset",
			"-YPadding:="		, "0",
			"+ZPaddingType:="	, "Percentage Offset",
			"+ZPadding:="		, "0",
			"-ZPaddingType:="	, "Percentage Offset",
			"-ZPadding:="		, "10"
		], 
		[
			"NAME:Attributes",
			"Name:="		, "Region",
			"Flags:="		, "Wireframe#",
			"Color:="		, "(143 175 143)",
			"Transparency:="	, 0,
			"PartCoordinateSystem:=", "Global",
			"UDMId:="		, "",
			"MaterialValue:="	, "\"vacuum\"",
			"SurfaceMaterialValue:=", "\"\"",
			"SolveInside:="		, True,
			"ShellElement:="	, False,
			"ShellElementThickness:=", "nan ",
			"IsMaterialEditable:="	, True,
			"UseMaterialAppearance:=", False,
			"IsLightweight:="	, False
		])
	oModule = oDesign.GetModule("AnalysisSetup")
	oModule.InsertSetup("HfssDriven", 
		[
			"NAME:Setup1",
			"SolveType:="		, "Single",
			# TODO: 2, 2.45, 3
			"Frequency:="		, frequency+"GHz",
			"MaxDeltaS:="		, 0.1,
			"UseMatrixConv:="	, False,
			"MaximumPasses:="	, 3,
			"MinimumPasses:="	, 1,
			"MinimumConvergedPasses:=", 1,
			"PercentRefinement:="	, 30,
			"IsEnabled:="		, True,
			[
				"NAME:MeshLink",
				"ImportMesh:="		, False
			],
			"BasisOrder:="		, 1,
			"DoLambdaRefine:="	, True,
			"DoMaterialLambda:="	, True,
			"SetLambdaTarget:="	, False,
			"Target:="		, 0.3333,
			"UseMaxTetIncrease:="	, False,
			"PortAccuracy:="	, 2,
			"UseABCOnPort:="	, False,
			"SetPortMinMaxTri:="	, False,
			"UseDomains:="		, False,
			"UseIterativeSolver:="	, False,
			"SaveRadFieldsOnly:="	, False,
			"SaveAnyFields:="	, True,
			"IESolverType:="	, "Auto",
			"LambdaTargetForIESolver:=", 0.15,
			"UseDefaultLambdaTgtForIESolver:=", True,
			"IE Solver Accuracy:="	, "Balanced"
		])
	oModule.InsertFrequencySweep("Setup1", 
		[
			"NAME:Sweep",
			"IsEnabled:="		, True,
			"RangeType:="		, "LinearCount",
			"RangeStart:="		, "2.4GHz",
			"RangeEnd:="		, "2.5GHz",
			"RangeCount:="		, 401,
			"Type:="		, "Interpolating",
			"SaveFields:="		, False,
			"SaveRadFields:="	, False,
			"InterpTolerance:="	, 0.5,
			"InterpMaxSolns:="	, 250,
			"InterpMinSolns:="	, 0,
			"InterpMinSubranges:="	, 1,
			"ExtrapToDC:="		, False,
			"InterpUseS:="		, True,
			"InterpUsePortImped:="	, False,
			"InterpUsePropConst:="	, True,
			"UseDerivativeConvergence:=", False,
			"InterpDerivTolerance:=", 0.2,
			"UseFullBasis:="	, True,
			"EnforcePassivity:="	, True,
			"PassivityErrorTolerance:=", 0.0001
		])
	# change
	oProject.SaveAs("C:\\Users\\USER\\Desktop\\Light test (HFSS)\\Light_test 20230502v2_copy.aedtresults.aedt", True)
	oDesign.AnalyzeAll()
	oModule = oDesign.GetModule("FieldsReporter")
	oModule.CreateFieldPlot(
		[
			"NAME:Mag_E1",
			"SolutionName:="	, "Setup1 : LastAdaptive",
			"UserSpecifyName:="	, 0,
			"UserSpecifyFolder:="	, 0,
			"QuantityName:="	, "Mag_E",
			"PlotFolder:="		, "E Field",
			"StreamlinePlot:="	, False,
			"AdjacentSidePlot:="	, False,
			"FullModelPlot:="	, False,
			"IntrinsicVar:="	, "Freq=\'2.4500000000000002GHz\' Phase=\'0deg\'",
			"PlotGeomInfo:="	, [1,"Surface","FacesList",1,"229"],
			"FilterBoxes:="		, [0],
			[
				"NAME:PlotOnSurfaceSettings",
				"Filled:="		, False,
				"IsoValType:="		, "Fringe",
				"AddGrid:="		, False,
				"MapTransparency:="	, True,
				"Refinement:="		, 0,
				"Transparency:="	, 0,
				"SmoothingLevel:="	, 0,
				"ShadingType:="		, 0,
				[
					"NAME:Arrow3DSpacingSettings",
					"ArrowUniform:="	, True,
					"ArrowSpacing:="	, 0,
					"MinArrowSpacing:="	, 0,
					"MaxArrowSpacing:="	, 0
				],
				"GridColor:="		, [255,255,255]
			],
			"EnableGaussianSmoothing:=", False
		], "Field")
	oModule = oDesign.GetModule("Solutions")
	oModule.EditSources(
		[
			[
				"IncludePortPostProcessing:=", False,
				"SpecifySystemPower:="	, False
			],
			[
				"Name:="		, "1:1",
				"Magnitude:="		, "700W",
				"Phase:="		, str(Waveport1_phase)+"deg"
			],
			[
				"Name:="		, "2:1",
				"Magnitude:="		, "700W",
				"Phase:="		, str(Waveport2_phase)+"deg"
			]
		])
	oModule = oDesign.GetModule("FieldsReporter")
	oModule.CopyNamedExprToStack("Mag_E")

	oModule.ExportOnGrid("C:\\Users\\USER\\Desktop\\Code\\Full_Flow\\Data\\output"+str(Iteration)+".fld", [str(grid_x_start)+"mm", str(grid_y_start)+"mm", str(grid_z_start)+"mm"], [str(grid_x_end)+"mm", str(grid_y_end)+"mm", str(grid_z_end)+"mm"], [str(GRID_SIZE)+"mm", str(GRID_SIZE)+"mm", str(GRID_SIZE)+"mm"], "Setup1 : LastAdaptive", 
		[
			"Freq:="		, str( frequency)+"GHz",
			"Phase:="		, "0deg"
		], True, "Cartesian", ["0mm", "0mm", "0mm"], False)

	# oDesktop.DeleteProject("Light_test 20230502v2_copy.aedtresults")


if __name__ ==  "__main__":

	for iteration in range(1):
		path = "C:/Users/USER/Desktop/Code/Full_Flow/Data/input"+str(iteration)+".txt"
		while not os.path.exists(path):
			time.sleep(1)
		with open(path) as f:
			for line in f.readlines():
				s = line.split(' ')
				Box_X = float(s[0])
				Box_Y = float(s[1])
				Box_Z = float(s[2])
				Waveport1_angle = float(s[3])
				Waveport1_position = "up"
				Waveport2_angle = float(s[5])
				Waveport2_position = "back"
				Waveport1_x = float(s[7])
				Waveport1_y = float(s[8])
				Waveport2_x = float(s[9])
				Waveport2_y = float(s[10])
				frequency = s[11]
				Waveport1_phase = s[12]
				Waveport2_phase = s[13]

		Simulation(Box_X, Box_Y, Box_Z, Waveport1_angle, Waveport1_position, Waveport2_angle, Waveport2_position, Waveport1_x, Waveport1_y, Waveport2_x, Waveport2_y, iteration, frequency, Waveport1_phase, Waveport2_phase)