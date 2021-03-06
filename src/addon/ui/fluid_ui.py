# Blender FLIP Fluid Add-on
# Copyright (C) 2019 Ryan L. Guy
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bpy

from ..utils import version_compatibility_utils as vcu


class FLIPFLUID_PT_FluidTypePanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "physics"
    bl_category = "FLIP Fluid"
    bl_label = "FLIP Fluid"


    @classmethod
    def poll(cls, context):
        obj_props = vcu.get_active_object(context).flip_fluid
        return obj_props.is_active and obj_props.object_type == 'TYPE_FLUID'


    def draw(self, context):
        obj = vcu.get_active_object(context)
        obj_props = obj.flip_fluid
        fluid_props = obj_props.fluid
        show_advanced = not vcu.get_addon_preferences(context).beginner_friendly_mode

        column = self.layout.column()
        column.prop(obj_props, "object_type")
        column.separator()

        if show_advanced:
            column.label(text="Trigger:")
            row = column.row(align= True)
            row.prop(fluid_props, "frame_offset_type", text = "")
            if fluid_props.frame_offset_type == 'OFFSET_TYPE_FRAME':
                row.prop(fluid_props, "frame_offset")
            elif fluid_props.frame_offset_type == 'OFFSET_TYPE_TIMELINE':
                row.prop(fluid_props, "timeline_offset")
            self.layout.separator()

        box = self.layout.box()
        box.label(text="Fluid Velocity Mode:")
        row = box.row(align=True)
        row.prop(fluid_props, "fluid_velocity_mode", expand=True)

        if fluid_props.fluid_velocity_mode == 'FLUID_VELOCITY_MANUAL':
            column = box.column(align=True)
            column.label(text="Fluid Velocity:")
            row = column.row(align=True)
            row.prop(fluid_props, "initial_velocity", text="")
        else:
            column = box.column(align=True)
            split = column.split(align=True)
            column_left = split.column(align=True)
            column_left.label(text="Fluid Speed:")
            column_left.prop(fluid_props, "initial_speed")

            target_collection = vcu.get_scene_collection()
            if vcu.is_blender_28():
                search_group = "all_objects"
            else:
                search_group = "objects"

            column_right = split.column(align=True)
            column_right.label(text="Target Object:")
            column_right.prop_search(fluid_props, "target_object", target_collection, search_group, text="")
            column_right.prop(fluid_props, "export_animated_target")

        if show_advanced:
            box.separator()
            column = box.column(align=True)
            split = vcu.ui_split(column, factor=0.66)
            column = split.column()
            column.prop(fluid_props, "append_object_velocity")
            column = split.column()
            column.enabled = fluid_props.append_object_velocity
            column.prop(fluid_props, "append_object_velocity_influence")

            column = self.layout.column()
            column.separator()
            split = column.split()
            column_left = split.column()
            column_left.prop(fluid_props, "export_animated_mesh")
            column_right = split.column()
            column_right.enabled = fluid_props.export_animated_mesh
            column_right.prop(fluid_props, "skip_animated_mesh_reexport")
    

def register():
    bpy.utils.register_class(FLIPFLUID_PT_FluidTypePanel)


def unregister():
    bpy.utils.unregister_class(FLIPFLUID_PT_FluidTypePanel)
