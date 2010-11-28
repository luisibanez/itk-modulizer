from vtk import *

reader1 = vtkXMLTreeReader()
reader1.SetFileName("itkModules.xml")
reader1.Update()

view = vtkTreeRingView()
view.SetRepresentationFromInput(reader1.GetOutput())
view.SetAreaSizeArrayName("size")
view.SetAreaColorArrayName("level")
view.SetAreaLabelArrayName("id")
view.SetAreaLabelVisibility(True)
view.SetAreaHoverArrayName("id")
view.SetShrinkPercentage(0.05)
view.Update()

theme = vtkViewTheme.CreateMellowTheme()
view.ApplyViewTheme(theme)
theme.FastDelete()

view.ResetCamera()
view.Render()

view.GetInteractor().Start()
