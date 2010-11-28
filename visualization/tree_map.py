from vtk import *

reader = vtkXMLTreeReader()
reader.SetFileName("itkModules.xml")
reader.Update()

numeric = vtkStringToNumeric()
numeric.SetInputConnection(reader.GetOutputPort())

view = vtkTreeMapView()
view.SetAreaSizeArrayName("size");
view.SetAreaColorArrayName("level");
view.SetAreaLabelArrayName("id");
view.SetAreaLabelVisibility(True);
view.SetAreaHoverArrayName("id");
view.SetLayoutStrategyToSquarify();
view.SetRepresentationFromInputConnection(numeric.GetOutputPort());

theme = vtkViewTheme.CreateMellowTheme()
view.ApplyViewTheme(theme)
theme.FastDelete()

view.ResetCamera()
view.Render()

view.GetInteractor().Start()
