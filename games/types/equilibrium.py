#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from games.types.game import Eq

class DomEq(Eq):
	def __init__(self, play):
		Eq.__init__(self, play)


class PureEq(Eq):
	def __init__(self, play):
		Eq.__init__(self, play)


class MixedEq(Eq):
	def __init__(self, play):
		Eq.__init__(self, play)


class CorEq(Eq):
	def __init__(self, play):
		Eq.__init__(self, play)


class CoarseEq(Eq):
	def __init__(self, play):
		Eq.__init__(self, play)