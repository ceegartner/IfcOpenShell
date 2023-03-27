# IfcOpenShell - IFC toolkit and geometry engine
# Copyright (C) 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of IfcOpenShell.
#
# IfcOpenShell is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IfcOpenShell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with IfcOpenShell.  If not, see <http://www.gnu.org/licenses/>.


class Data:
    is_loaded = False
    profiles = {}

    @classmethod
    def purge(cls):
        cls.is_loaded = False
        cls.profiles = {}

    @classmethod
    def load(cls, file):
        if not file:
            return
        cls.profiles = {}
        for profile in file.by_type("IfcProfileDef"):
            cls.profiles[profile.id()] = profile.get_info()
        cls.is_loaded = True