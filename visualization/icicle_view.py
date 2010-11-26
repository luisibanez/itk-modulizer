from vtk import *

reader = vtkXMLTreeReader()
reader.SetFileName("itkmodules.xml")
reader.Update()

view = vtkIcicleView()
view.SetRepresentationFromInput(reader.GetOutput())
view.SetAreaSizeArrayName("size")
view.SetAreaColorArrayName("vertex id")
view.SetAreaLabelArrayName("id")
view.SetAreaLabelVisibility(True)
view.SetAreaHoverArrayName("id")
view.SetRootWidth(20.)
view.Update()

theme = vtkViewTheme.CreateMellowTheme()
view.ApplyViewTheme(theme)
theme.FastDelete()

view.ResetCamera()
view.Render()

view.GetInteractor().Initialize()
view.GetInteractor().Start()
