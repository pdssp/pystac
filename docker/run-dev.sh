#!/bin/sh
# pySTAC - Library implementing STAC protocole
# Copyright (C) 2021 - CNES (Jean-Christophe Malapert for Pôle Surfaces Planétaires)
#
# This file is part of pySTAC.
#
# pySTAC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pySTAC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pySTAC.  If not, see <https://www.gnu.org/licenses/>.
set search
set ps

search=`docker images | grep dev/pystac | wc -l`
if [ $search = 0 ];
then
	# only the heaader - no image found
	echo "Please build the image by running 'make docker-container-dev'"
	exit 1
fi

ps=`docker ps -a | grep develop-pystac | wc -l`
if [ $ps = 0 ];
then
	echo "no container available, start one"
	docker run --name=develop-pystac #\
		#-v /dev:/dev \
		#-v `echo ~`:/home/${USER} \
		#-v `pwd`/data:/srv/pystac/data \
		#-p 8082:8082 \
		-it dev/pystac /bin/bash
	exit $?
fi

ps=`docker ps | grep develop-pystac | wc -l`
if [ $ps = 0 ];
then
	echo "container available but not started, start and go inside"
	docker start develop-pystac
	docker exec -it develop-pystac /bin/bash
else
	echo "container started, go inside"
	docker exec -it develop-pystac /bin/bash
fi
