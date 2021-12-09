###############################################################################
#
#	Involution Tool
#	File: Makefile
#	
#   Copyright (C) 2018-2021  Daniel OEHLINGER <d.oehlinger@outlook.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################

all: compile_c

# python_channel.o: python_channel.c
# 	gcc -c -I/opt/mentor_modelsim-10.5c/modeltech/include -I/opt/rh/rh-python36/root/usr/include/python3.6m -fPIC  -Wsign-compare -I/opt/rh/rh-python36/root/usr/include -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv   -DDYNAMIC_ANNOTATIONS_ENABLED=1 -DNDEBUG -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv python_channel.c

compile_c: python_channel.c	
	gcc -c -I/opt/mentor_modelsim-10.5c/modeltech/include -I/opt/rh/rh-python36/root/usr/include/python3.6m -fPIC  -Wsign-compare -I/home/s01525898/.local/lib/python3.6/site-packages/numpy/core/include/numpy -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv   -DDYNAMIC_ANNOTATIONS_ENABLED=1 -DNDEBUG -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv python_channel.c
	ld -L/opt/rh/rh-python36/root/usr/lib64 -lpython3.6m -lpthread -ldl  -lutil -lrt -lm -export-dynamic -shared -E -o python_channel.so python_channel.o

# Not working yet
# python_channel: python_channel.o
# 	ld -L/opt/rh/rh-python36/root/usr/lib64 -lpython3.6m -lpthread -ldl  -lutil -lrt -lm -export-dynamic -o python_channel python_channel.o --entry main

clean:
	rm -f python_channel.o
	rm -f python_channel.so
	rm -f python_channel

.PHONY: all
.PHONY: clean
.PHONY: compile_c

