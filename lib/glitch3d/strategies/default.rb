# frozen_string_literal: true
module Glitch3d
  class Default
    class << self
      def alter_vertices(vertices_objects_array)
        (VERTEX_GLITCH_ITERATION_RATIO * vertices_objects_array.size).to_i.times do |_|
          vertices_objects_array.sample.fuck
        end
        vertices_objects_array
      end

      def alter_faces(faces_objects_array, vertex_objects_array)
        faces_objects_array
      end
    end
  end
end
