from vtk import *

reader1 = vtkXMLTreeReader()
reader1.SetFileName("itkModules.xml")
reader1.Update()

view = vtkTreeMapView()
view.SetAreaSizeArrayName("size")
view.SetAreaColorArrayName("level")
view.SetAreaLabelArrayName("id")
view.SetAreaLabelVisibility(True)
view.SetAreaHoverArrayName("id")
view.SetLayoutStrategyToSquarify()
view.SetRepresentationFromInput(reader1.GetOutput())

theme = vtkViewTheme.CreateMellowTheme()
view.ApplyViewTheme(theme)
theme.FastDelete()

view.ResetCamera()
view.Render()

view.GetInteractor().Start()
