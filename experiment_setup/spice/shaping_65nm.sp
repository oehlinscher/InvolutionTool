*--------------------------------------------------------------------------------
*
*	Involution Tool
*	File: shaping_65nm.sp
*	
*  Copyright (C) 2018-2019  Daniel OEHLINGER <d.oehlinger@outlook.com>
*
*  This source file may be used and distributed without restriction provided
*  that this copyright statement is not removed from the file and that any
*  derivative work contains the original copyright notice and the associated
*  disclaimer.
*
*  This source file is free software: you can redistribute it and/or modify it
*  under the terms of the GNU Lesser General Public License as published by
*  the Free Software Foundation, either version 3 of the License, or (at your
*  option) any later version.
*
*  This source file is distributed in the hope that it will be useful, but
*  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
*  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
*  for more details.
*
*  You should have received a copy of the GNU Lesser General Public License
*  along with the noasic library.  If not, see http://www.gnu.org/licenses
*
*--------------------------------------------------------------------------------


.subckt shaping
+ in out shapevdd 
Xg10 temp1 in shapevdd 0 0 shapevdd CKINVM1N
Xg11 out temp1 shapevdd 0 0 shapevdd CKINVM1N

* C after inverters against GND
C1 temp1 0 0.0008pF
C2 out 0 0.0008pF

.ends
