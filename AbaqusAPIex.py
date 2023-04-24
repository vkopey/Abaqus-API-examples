# -*- coding: utf-8 -*-
u"""Abaqus CAE API example
Приклад демонструє можливість автоматичної побудови моделі, симуляції і отримання результатів. Дозволяє організувати автоматичні параметричні дослідження і оптимізації.
"""
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

# функція отримує значення параметрів моделі x та виводить або повертає результати
def f(*x):
    # Параметричний ескіз моделі може будуватись за допомогою коду або завантажуватись з файлу. Цей код будує ескіз моделі.
    """
    Mdb()
    m=mdb.models['Model-1']
    
    s=m.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g,v=s.geometry, s.vertices
    s.sketchOptions.setValues(viewStyle=AXISYM)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.Line(point1=(0.0, 0.0), point2=(0.0, 30.2430419921875))
    s.VerticalConstraint(addUndoState=False, entity=g[3])
    s.ParallelConstraint(addUndoState=False, entity1=g[2], entity2=g[3])
    s.CoincidentConstraint(addUndoState=False, entity1=v[0], entity2=g[2])
    s.CoincidentConstraint(addUndoState=False, entity1=v[1], entity2=g[2])
    s.Line(point1=(0.0,30.2430419921875), point2=(10.0, 30.2430419921875))
    s.HorizontalConstraint(addUndoState=False, entity=g[4])
    s.PerpendicularConstraint(addUndoState=False, entity1=g[3], entity2=g[4])
    s.Line(point1=(10.0, 30.2430419921875), point2=(10.0, 20.0))
    s.VerticalConstraint(addUndoState=False, entity=g[5])
    s.PerpendicularConstraint(addUndoState=False, entity1=g[4], entity2=g[5])
    s.Line(point1=(10.0, 20.0), point2=(5.0, 15.0))
    s.Line(point1=(5.0, 15.0), point2=(10.0, 10.0))
    s.PerpendicularConstraint(addUndoState=False, entity1=g[6], entity2=g[7])
    s.Line(point1=(10.0, 10.0), point2=(10.0, 0.0))
    s.VerticalConstraint(addUndoState=False, entity=g[8])
    s.Line(point1=(10.0, 0.0), point2=(0.0, 0.0))
    s.HorizontalConstraint(addUndoState=False, entity=g[9])
    s.PerpendicularConstraint(addUndoState=False, entity1=g[8], entity2=g[9])
    s.FixedConstraint(entity=v[0])
    s.VerticalDimension(textPoint=(-3.2730655670166, 18.5634937286377), value=x[0], vertex1=v[0], vertex2=v[1]) #d[0].setValues(value=30, )
    s.HorizontalDimension(textPoint=(6.21212959289551, 32.5262603759766), value=10.0, vertex1=v[1], vertex2=v[2])
    s.HorizontalDimension(textPoint=(6.56343269348145, 21.9883232116699), value=5.0, vertex1=v[4], vertex2=v[3])
    s.EqualLengthConstraint(entity1=g[7], entity2=g[6])
    s.EqualLengthConstraint(entity1=g[8], entity2=g[5])
    s.EqualLengthConstraint(entity1=g[4], entity2=g[9])
    """
    
    # А цей код завантажує ескіз з файлу (закоментуйте його, якщо використовуєте код вище)
    openMdb(pathName='C:/Temp/AbaqusAPIex.cae')
    m=mdb.models['Model-1']
    s = m.ConstrainedSketch(name='__edit__', objectToCopy=m.sketches['Sketch-1'])
    d=s.dimensions
    d[0].setValues(value=x[0], )
    m.sketches.changeKey(fromName='__edit__', toName='Sketch-1')

    # побудова моделі і симуляція
    p=m.Part(dimensionality=AXISYMMETRIC, name='Part-1', type=DEFORMABLE_BODY)
    p.BaseShell(sketch=s)
    del s
    m.Material(name='Material-1')
    m.materials['Material-1'].Elastic(table=((200000000000.0, 0.3), ))
    m.HomogeneousSolidSection(material='Material-1', name='Section-1', thickness=None)
    p.Set(faces=p.faces.getSequenceFromMask(('[#1 ]', ), ), name='Set-1')
    p.SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        p.sets['Set-1'], sectionName=
        'Section-1', thicknessAssignment=FROM_SECTION)
    m.rootAssembly.DatumCsysByThreePoints(coordSysType=
        CYLINDRICAL, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(0.0, 
        0.0, -1.0))
    m.rootAssembly.Instance(dependent=ON, name='Part-1-1', part=p)
    m.StaticStep(name='Step-1', previous='Initial')
    m.rootAssembly.Set(edges=
        m.rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
        ('[#1 ]', ), ), name='Set-1')
    m.rootAssembly.Set( vertices=m.rootAssembly.instances['Part-1-1'].vertices.getSequenceFromMask(('[#8 ]', ), ),name='Set-2')
    m.EncastreBC(createStepName='Step-1', localCsys=None, name=
        'BC-1', region=m.rootAssembly.sets['Set-1'])
    m.rootAssembly.Surface(name='Surf-1', side1Edges=
        m.rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
        ('[#20 ]', ), ))
    mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, field='', magnitude=-100000000.0, name='Load-1', 
        region=m.rootAssembly.surfaces['Surf-1'])
    p.seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=1.0)
    p.generateMesh()
    m.rootAssembly.regenerate()
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
        numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
        ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
    mdb.jobs['Job-1'].waitForCompletion()
    
    # читання результатів
    odb = session.openOdb(name='C:/Temp/Job-1.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=odb)
    xy=session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('S', INTEGRATION_POINT, ((INVARIANT, 'Mises'), )), ), nodeSets=('SET-2', ))
    #xy=session.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT, variable=(('S', INTEGRATION_POINT, ((INVARIANT, 'Mises'), )), ), elementSets=('SET-1', ))
    print xy[0].data
    odb.close()

# головний цикл параметричного дослідження
for x in [25,30,35]:
    f(x)