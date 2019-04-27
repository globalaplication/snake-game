#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
GObject.threads_init()
import random
snake = {"dikey":25, "yatay":20, "genislik":13, "yukseklik":13, 
		"zamanlayici":125}
class main(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		self.set_title("Yilan Oyunu")
		self.connect("destroy", Gtk.main_quit)
		self.connect("key-press-event", self.push)
		GObject.timeout_add(snake.get("zamanlayici"), self.timer)
		self.mainbox = Gtk.VBox(margin=0)
		self.mainbox.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("black"))
		self.add(self.mainbox)
		self.top = Gtk.HBox(valign=1, halign=1, margin=10)
		self.mainbox.pack_start(self.top, 0,0,10)
		self.bottom = Gtk.HBox()
		self.mainbox.add(self.bottom)
		self.left = Gtk.VBox(margin=5)
		self.left.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("gray"))
		self.bottom.add(self.left)
		self.right = Gtk.VBox(valign=1)
		self.bottom.add(self.right)
		self.puanTitle = Gtk.Label()
		global puan, step
		puan = 0
		step = 0
		self.dikeyKonumEntry = Gtk.Entry(text=5)
		self.yatayKonumEntry = Gtk.Entry(text=7)
		self.boxs = {}
		for i in range(1, snake.get("dikey")+1):
			self.boxs.update({i:[-1,]})
		self.klavye = None
		self.yilan = [[5,7], [6,7], [7,7], [8,7]]
		self.uzunluk = 4
		self.runtimer = True
	def draw(self):
		for dikey in range(1, snake.get("dikey")+1):
			hbox = Gtk.HBox()
			self.left.pack_start(hbox, 0,0,1)
			for yatay in range(1, snake.get("yatay")+1):
				box = Gtk.Box()
				box.modify_bg(0, Gdk.color_parse("black"))
				box.set_size_request(snake.get("genislik"),
				snake.get("yukseklik"))
				hbox.pack_start(box, 0,0,1)
				self.boxs.get(dikey).append(box)
		self.top.add(self.puanTitle)
		self.right.add(self.dikeyKonumEntry)
		self.right.add(self.yatayKonumEntry)
	def push(self, keyboard, event):
		if self.klavye != 65363 and event.keyval == 65361: #sol TUS
			self.klavye = 65361
		elif self.klavye != 65361 and event.keyval == 65363: #sag TUS
			self.klavye = 65363
		elif self.klavye != 65364 and event.keyval == 65362: #yukari TUS
			self.klavye = 65362
		elif self.klavye != 65362 and event.keyval == 65364: #asagi TUS
			self.klavye = 65364
	def timer(self):
		global puan, step
		if self.klavye is not  None: step = step + 1
		self.puanTitle.set_markup("""<span color='white'><b>Strawberry:</b></span><span color='white'> {} </span>
<span color='white'><b>Step:</b></span><span color='white'> {} </span>""".format(
			str(puan), step))
		if self.klavye == 65361 :
			self.yatayKonumEntry.set_text(str(int(self.yatayKonumEntry.get_text())-1))
		if self.klavye == 65363 :
			self.yatayKonumEntry.set_text(str(int(self.yatayKonumEntry.get_text())+1))
		if self.klavye == 65362 :
			self.dikeyKonumEntry.set_text(str(int(self.dikeyKonumEntry.get_text())-1))
		if self.klavye == 65364 :
			self.dikeyKonumEntry.set_text(str(int(self.dikeyKonumEntry.get_text())+1))
		dikey, yatay = int(self.dikeyKonumEntry.get_text()), int(self.yatayKonumEntry.get_text())
		if [dikey, yatay] in self.yilan[1:self.uzunluk]:
			print "game over!"
			self.runtimer = False
		if strawberry == [dikey, yatay]:
			puan = puan + 1
			self.uzunluk = self.uzunluk + 2
			self.strew()
		if [dikey , yatay] not in self.yilan[0:self.uzunluk]:
			if yatay is 0 : #sol
				dikey, yatay = int(self.dikeyKonumEntry.get_text()), snake.get("yatay")
				self.dikeyKonumEntry.set_text(str(dikey))
				self.yatayKonumEntry.set_text(str(yatay))
			if yatay is snake.get("yatay")+1 :  #sag
				dikey, yatay = int(self.dikeyKonumEntry.get_text()), 1
				self.dikeyKonumEntry.set_text(str(dikey))
				self.yatayKonumEntry.set_text(str(yatay))
			if dikey is 0 : #yukari
				dikey, yatay = int(snake.get("dikey")), int(self.yatayKonumEntry.get_text())
				self.dikeyKonumEntry.set_text(str(dikey))
				self.yatayKonumEntry.set_text(str(yatay))
			if dikey is snake.get("dikey")+1 : #asagi
				dikey, yatay = 1, int(self.yatayKonumEntry.get_text())
				self.dikeyKonumEntry.set_text(str(dikey))
				self.yatayKonumEntry.set_text(str(yatay))
			self.yilan.insert(0, [dikey, yatay])
			dikey ,yatay = self.yilan[self.uzunluk]
			self.boxs.get(dikey)[yatay].modify_bg(0, Gdk.color_parse("black"))
		for enum, position in enumerate(self.yilan[0:self.uzunluk], 1):
			dikey , yatay = position
			if enum is 1:
				self.boxs.get(dikey)[yatay].modify_bg(0, Gdk.color_parse("red"))
				#yilan bas rengi <red>
			else:
				self.boxs.get(dikey)[yatay].modify_bg(0, Gdk.color_parse("gray"))
				#yilan kuyruk rengi <white>
		return self.runtimer
	def strew(self):
		global strawberry
		for strew in range(10):
			dikey = random.choice(range(1,snake.get("dikey")))
			yatay = random.choice(range(1,snake.get("yatay")))
			if [dikey, yatay] not in self.yilan[0:self.uzunluk]:
				strawberry = [dikey, yatay]
				self.boxs.get(dikey)[yatay].modify_bg(0, Gdk.color_parse("red"))
				#cilek rengi <red>
				break
	def hide(self):
		self.right.hide()
		self.set_resizable(False)
	def about():
		return
win = main()
win.draw()
win.strew()
win.show_all()
win.hide()
Gtk.main()
