# Matthew Plummer Fernandez hommage
# Draw interesting parametric curves and instantiate meshes on its path
import sys, code, random, os, math, bpy, canvas, mathutils

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import helpers

class Fernandez(canvas.Canvas):
  MESH_OCCURENCE = 1 # 1 mesh every X point of the curve

  FUNCTIONS = [
    # decorated knot (can expand to 20 units)
    [
      lambda t: math.cos( 2 * t * math.pi * 2 ) * ( 1 + 0.45 * math.cos( 3 * t * math.pi * 2 ) + 0.4 * math.cos( 9 * t * math.pi * 2 ) ),
      lambda t: math.sin( 2 * t * math.pi * 2 ) * ( 1 + 0.45 * math.cos( 3 * t * math.pi * 2 ) + 0.4 * math.cos( 9 * t * math.pi * 2 ) ),
      lambda t: 0.2 * math.sin( 9 * t * math.pi * 2 )
    ],
    # another knot like structure
    [
      lambda t: 10 * (math.cos(t) + math.cos(3 * t)) + math.cos(2 * t) + math.cos(4 * t),
      lambda t: 6 * math.sin(t) + 10 * math.sin(3 * t),
      lambda t: 4 * math.sin(3 * t) * math.sin(5 * t / 2) + 4 * math.sin(4 * t) - 2 * math.sin(6 * t)
    ],
    # Some weird sphere like structure (contained within a 1x1x1 cube)
    [
      lambda t: math.sin(t) * math.cos(20*t),
      lambda t: math.sin(t) * math.sin(20*t),
      lambda t: math.cos(t)
    ],
    # Some weird funnel like structure (contained within a 1x1x1 cube)
    [
      lambda t: math.sin(t) * math.cos(20*t),
      lambda t: math.sin(t) * math.sin(20*t),
      lambda t: math.sin(t)
    ]
  ]

  def render(self):
    base_particle = helpers.infer_primitive(random.choice(self.PRIMITIVES), location = (100, 100, 100), radius=1)
    art = self.matthew_curve(self.SUBJECT, 20)
    self.spawn_particles_system(art, base_particle)

    for f in range(self.NUMBER_OF_FRAMES):
      bpy.context.scene.frame_set(f)
      art.particle_systems["ParticleSystem"].seed += 1
      settings = bpy.data.particles[-1]
      settings.particle_size += 0.005
      art.scale += mathutils.Vector((0.02,0.02,0.02))
      helpers.add_frame([art], ['particle_systems["ParticleSystem"].seed', 'scale'])
      helpers.add_frame([settings], ['particle_size'])

  def rand_curve(self):
    return random.choice(self.FUNCTIONS)

  def matthew_curve(self, obj, time, scale = 0.2):
    fx, fy, fz = self.rand_curve()
    verts =  [(fx(t), fy(t), fz(t)) for t in helpers.pitched_array(0, time, 0.2)]
    bpy.context.scene.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')
    for idx, coord in enumerate(verts[0::self.MESH_OCCURENCE]):
      new_obj = helpers.duplicate_object(obj)
      new_obj.select = True
      new_obj.location = coord
      new_obj.scale = (0.02,0.02,0.02) if idx % 2 == 0 else (0.05, 0.05, 0.05)
      new_obj.rotation_euler.z += idx * (2 * math.pi) / len(verts)
      bpy.context.scene.objects.active = new_obj
    bpy.ops.object.join()
    res = bpy.context.object
    res.name = 'fernandez'
    helpers.resize(res)
    helpers.center(res)
    helpers.decimate(res)
    helpers.assign_material(res, helpers.random_material(self.MATERIALS_NAMES))
    support = helpers.create_mesh('fernandez_support', verts, [], (0,0,0),  [[v, v+1] for v in range(0, (len(verts) - 1))])
    helpers.resize(support)
    helpers.center(support)
    helpers.extrude(support)
    helpers.assign_material(support, helpers.random_material(self.MATERIALS_NAMES))
    return res

  def spawn_particles_system(self, base, obj):
    base.modifiers.new("Particles", type='PARTICLE_SYSTEM')
    settings = bpy.data.particles[-1]
    settings.emit_from = 'VERT'
    settings.physics_type = 'NO'
    settings.count = 2000 # default 1000
    settings.particle_size = 0.01
    settings.render_type = 'OBJECT'
    settings.dupli_object = obj
    settings.show_unborn = True
    settings.use_dead = True
    settings.size_random = 0.5
    bpy.ops.object.duplicates_make_real()
