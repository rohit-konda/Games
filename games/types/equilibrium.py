#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Parent classes for types of equilibrium
"""

from games.types.game import Eq

class DomEq(Eq):

	"""Strictly Dominating Equilibrium
	"""

	def __init__(self, play):
		Eq.__init__(self, play)


class PureEq(Eq):

	"""Pure Nash Equilibrium.
	"""

	def __init__(self, play):
		Eq.__init__(self, play)


class MixedEq(Eq):

	"""Mixed Nash equilibrium.
	"""

	def __init__(self, play):
		Eq.__init__(self, play)


class CorEq(Eq):

	"""Correlated Equilibrium.
	"""

	def __init__(self, play):
		Eq.__init__(self, play)


class CoarseEq(Eq):

	"""Coarse Correlated Equilibrium.
	"""

	def __init__(self, play):
		Eq.__init__(self, play)