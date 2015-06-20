# Copyright 2011, Thomas G. Dimiduk
#
# This file is part of GroupEng.
#
# GroupEng is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GroupEng is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with GroupEng.  If not, see <http://www.gnu.org/licenses/>.

from .student import Student

class Course(object):
    def __init__(self, students, group_size='3+', uneven_size=None):
        self.students = students
        self.students_no_phantoms = list(students)

        # parse group size
        try:
            self.group_size = int(group_size)
            if uneven_size.lower() == 'high':
                self.uneven_size = '+'
            elif self.uneven_size.lower() == 'low':
                self.uneven_size = '-'
            else:
                # no uneven_size specified, use default based on group size
                if self.group_size < 4:
                    self.uneven_size = '+'
                else:
                    self.uneven_size = '-'
        except ValueError:
            if group_size[-1] in '+-':
                self.uneven_size = group_size[-1]
                self.group_size = int(group_size[:-1])
            else:
                raise Exception("{0} cannot be interpreted as a group size".format(group_size))

        self.n_groups = len(students) // self.group_size

        #TODO: check carefully that things are handled correctly in the case
        #where len(students) divides evenly into increased group size.
        remainder = len(students) % self.group_size
        if remainder:
            if self.uneven_size == '+':
                # add 1 to group size so most groups can have a phantom
                self.group_size += 1
        else:
            self.uneven_size = '='

        if (self.n_groups * self.group_size) < len(students):
            self.n_groups += 1

        if self.uneven_size != '=':
            phantoms_needed = self.group_size * self.n_groups - len(self.students)
            def make_phantom():
                data = dict([(key, None) for key in self.students[0].data.keys()])
                identifier = self.students[0].identifier
                data[identifier] = 'phantom'
                return Student(data, identifier=identifier, headers =
                               self.students[0].headers)

            self.students += [make_phantom() for i in range(phantoms_needed)]
