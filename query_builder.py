#! /usr/bin/python
#
# DESCRIPTION:	
# AUTHOR: 	Mohamed Osama (mohamed.osama.aboelkheir@gmail.com)
# CREATED: 	Wed 23-Mar-2013
# LAST REVISED:	Wed 22-Mar-2014
#
##############
# DISCLAIMER #
##############
# Anyone is free to copy, modify, use, or distribute this script for any purpose, and by any means. However, Please take care THIS IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND AND YOU SHOULD USE IT AT YOUR OWN RISK.

from gi.repository import Gtk,Gdk
import re
import ConfigParser

class query_builder:

	def __init__(self):
		
		# read and intialize config file
		self.conf="query_builder.conf"
		self.Config=  ConfigParser.ConfigParser()
		self.Config.read(self.conf)
		
		# read and initialize Gtk window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("query_builder.glade")
		self.win = self.builder.get_object("window1")
		
		# intialize clipboard
		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		self.automatic_copy_check = self.builder.get_object("automatic_copy_check")
		
		# get ticket ids object
		self.ticket_ids = self.builder.get_object("ticket_ids")
		
		# get generate query button and text entry to display query
		self.generate_query_button = self.builder.get_object("Generate_query")
		self.query = self.builder.get_object("query")
		
		# get priority check boxes
		self.pAll_check=self.builder.get_object("pAll_check")
		self.p1_check=self.builder.get_object("p1_check")
		self.p2_check=self.builder.get_object("p2_check")
		self.p3_check=self.builder.get_object("p3_check")
		self.p4_check=self.builder.get_object("p4_check")
		
		# when priorities checked 
		prio_list=[self.p1_check,self.p2_check,self.p3_check,self.p4_check]
		prio_all=self.pAll_check
		self.p1_check.connect("toggled",self.standard_check,prio_list,prio_all)
		self.p2_check.connect("toggled",self.standard_check,prio_list,prio_all)
		self.p3_check.connect("toggled",self.standard_check,prio_list,prio_all)
		self.p4_check.connect("toggled",self.standard_check,prio_list,prio_all)
		self.pAll_check.connect("toggled",self.all_check,prio_list,prio_all)
		
		# get status checkboxes
		self.sAll_check=self.builder.get_object("sAll_check")
		self.sA_check=self.builder.get_object("sA_check")
		self.sI_check=self.builder.get_object("sI_check")
		self.sP_check=self.builder.get_object("sP_check")
		self.sR_check=self.builder.get_object("sR_check")
		self.sC_check=self.builder.get_object("sC_check")
		self.sN_check=self.builder.get_object("sN_check")
		
		# when status checked
		stat_list=[self.sA_check,self.sI_check,self.sP_check,self.sR_check,self.sC_check,self.sN_check]
		stat_all=self.sAll_check
		self.sA_check.connect("toggled",self.standard_check,stat_list,stat_all)
		self.sI_check.connect("toggled",self.standard_check,stat_list,stat_all)
		self.sP_check.connect("toggled",self.standard_check,stat_list,stat_all)
		self.sR_check.connect("toggled",self.standard_check,stat_list,stat_all)
		self.sC_check.connect("toggled",self.standard_check,stat_list,stat_all)
		self.sN_check.connect("toggled",self.standard_check,stat_list,stat_all)
		self.sAll_check.connect("toggled",self.all_check,stat_list,stat_all)
		
		# get type checkboxes
		self.tAll_check=self.builder.get_object("tAll_check")
		self.tINC_check=self.builder.get_object("tINC_check")
		self.tSR_check=self.builder.get_object("tSR_check")
		
		# when type checkboxes checked
		type_list=[self.tINC_check,self.tSR_check]
		type_all=self.tAll_check
		self.tINC_check.connect("toggled",self.standard_check,type_list,type_all)
		self.tSR_check.connect("toggled",self.standard_check,type_list,type_all)
		self.tAll_check.connect("toggled",self.all_check,type_list,type_all)
		
		# get Mont/Cust checkboxes
		self.mcAll_check=self.builder.get_object("mcAll_check")
		self.mcMONT_check=self.builder.get_object("mcMONT_check")
		self.mcCUST_check=self.builder.get_object("mcCUST_check")
		
		# when Mont/Cust checkboxes checked
		mc_list=[self.mcMONT_check,self.mcCUST_check]
		mc_all= self.mcAll_check
		self.mcMONT_check.connect("toggled",self.standard_check,mc_list,mc_all)
		self.mcCUST_check.connect("toggled",self.standard_check,mc_list,mc_all)
		self.mcAll_check.connect("toggled",self.all_check,mc_list,mc_all)
				
		# get SLA status checkboxes
		self.slaMet_check=self.builder.get_object("slaMet_check")
		self.slaWar_check=self.builder.get_object("slaWar_check")
		self.slaBre_check=self.builder.get_object("slaBre_check")
		self.slaNon_check=self.builder.get_object("slaNon_check")
		self.slaAll_check=self.builder.get_object("slaAll_check")
		
		# when SLA status checkboxes checked
		sla_list=[self.slaMet_check,self.slaWar_check,self.slaBre_check,self.slaNon_check]
		sla_all=self.slaAll_check
		self.slaMet_check.connect("toggled",self.standard_check,sla_list,sla_all)
		self.slaWar_check.connect("toggled",self.standard_check,sla_list,sla_all)
		self.slaBre_check.connect("toggled",self.standard_check,sla_list,sla_all)
		self.slaNon_check.connect("toggled",self.standard_check,sla_list,sla_all)
		self.slaAll_check.connect("toggled",self.all_check,sla_list,sla_all)
		
		# get service horizontal box
		self.box_service=self.builder.get_object("box_service")
		self.service_list=[eval(i[1]) for i in self.Config.items('Service')]
		self.service_check={}
		for i in self.service_list:
			self.service_check[i[0]]=Gtk.CheckButton(i[0],active=True)
			self.box_service.pack_start(self.service_check[i[0]], False, False, 0)
		
		self.srv_all=self.builder.get_object("srvAll_check")
		srv_all=self.srv_all
		srv_list=self.service_check.values()
		for srv in srv_list:
			srv.connect("toggled",self.standard_check,srv_list,srv_all)
		self.srv_all.connect("toggled",self.all_check,srv_list,srv_all)	

		# get Assigned Groups horizontal box
		self.box_teams=self.builder.get_object("box_teams")
		self.teams_list=[eval(i[1]) for i in self.Config.items('Teams')]
		self.teams_check={}
		for i in self.teams_list:
		    self.teams_check[i[0]]=Gtk.CheckButton(i[0],active=True)
		    self.box_teams.pack_start(self.teams_check[i[0]], False, False, 0)
		
		self.ag_all=self.builder.get_object("agAll_check")
		ag_all=self.ag_all
		ag_list=self.teams_check.values()
		for ag in ag_list:
		    ag.connect("toggled",self.standard_check,ag_list,ag_all)
		self.ag_all.connect("toggled",self.all_check,ag_list,ag_all)
		
		# get Company horizontal box
		self.box_company=self.builder.get_object("box_company")
		self.company_list=[eval(i[1]) for i in self.Config.items('Company')]
		self.company_check={}
		for i in self.company_list:
		    self.company_check[i[0]]=Gtk.CheckButton(i[0],active=True)
		    self.box_company.pack_start(self.company_check[i[0]], False, False, 0)
		
		self.c_all=self.builder.get_object("cAll_check")
		c_all=self.c_all
		c_list=self.company_check.values()
		for c in c_list:
		    c.connect("toggled",self.standard_check,c_list,c_all)
		self.c_all.connect("toggled",self.all_check,c_list,c_all)
		
		# Submit Date checkboxes and entries
		self.subd_start_check=self.builder.get_object("subd_start_check")
		self.subd_end_check=self.builder.get_object("subd_end_check")
		self.subd_start_entry=self.builder.get_object("subd_start_entry")
		self.subd_end_entry=self.builder.get_object("subd_end_entry")
		
		# when Submit Date checkboxes chedked
		self.subd_start_check.connect("toggled",self.date_check,self.subd_start_entry)
		self.subd_end_check.connect("toggled",self.date_check,self.subd_end_entry)
		
		# Modified Date checkboxes and entries
		self.modd_start_check=self.builder.get_object("modd_start_check")
		self.modd_end_check=self.builder.get_object("modd_end_check")
		self.modd_start_entry=self.builder.get_object("modd_start_entry")
		self.modd_end_entry=self.builder.get_object("modd_end_entry")
		
		# when Submit Date checkboxes chedked
		self.modd_start_check.connect("toggled",self.date_check,self.modd_start_entry)
		self.modd_end_check.connect("toggled",self.date_check,self.modd_end_entry)
		
		# Resolved Date checkboxes and entries
		self.resd_start_check=self.builder.get_object("resd_start_check")
		self.resd_end_check=self.builder.get_object("resd_end_check")
		self.resd_start_entry=self.builder.get_object("resd_start_entry")
		self.resd_end_entry=self.builder.get_object("resd_end_entry")
		
		# when Submit Date checkboxes chedked
		self.resd_start_check.connect("toggled",self.date_check,self.resd_start_entry)
		self.resd_end_check.connect("toggled",self.date_check,self.resd_end_entry)
		
		# when button clicked
		self.generate_query_button.connect("clicked", self.generate_query)
		
		# Menu Bar - File - reset
		self.reset_button=self.builder.get_object("reset_button")
		self.reset_button.connect("activate",self.reset)
		# Container for all checkboxes
		self.check_container=[prio_all]+prio_list+[stat_all]+stat_list+[type_all]+type_list+[mc_all]+mc_list+[sla_all]+sla_list+[srv_all]+srv_list+[ag_all]+ag_list+[c_all]+c_list
		
		# Menu Bar - File - quit
		self.quit_button=self.builder.get_object("quit_button")
		self.quit_button.connect("activate",self.quit)
		
		# Menu Bar - Help - about
		self.about_button=self.builder.get_object("about_button")
		self.about_button.connect("activate",self.about)
		
		# Display Window
		self.win.connect("delete-event", Gtk.main_quit)
		self.win.show_all()
		Gtk.main()

	
	def all_check(self,widget,list_check,all_check):
		active=[i.get_active() for i in list_check]
		if all_check.get_active():
			for i in list_check:
				i.set_active(1)
		elif all(active):
			all_check.set_active(1) 

	def standard_check(self,widget,list_check,all_check):
		active=[i.get_active() for i in list_check]
		if not all(active):
			all_check.set_active(0)
		else:
			all_check.set_active(1)
		if active.count(True)==0:
			widget.set_active(1)

	def date_check(self,widget,entry):
		if widget.get_active():
			entry.set_editable(1)
		else:
			entry.set_editable(0)
			entry.set_text("")
			

	def generate_query(self,widget, data=None):

		self.queries=[]

		# Ticket ids
		ticket_ids_txt=self.ticket_ids.get_buffer()
		start,end=ticket_ids_txt.get_bounds()
		ticket_ids_txt=ticket_ids_txt.get_text(start,end,include_hidden_chars=True)
		#print ticket_ids_txt
		ticket_ids_lst=list(set(["\'Incident ID*+\' = \""+i.group(0)+"\"" for i in re.finditer("INC[0-9]+",ticket_ids_txt)]))
		if len(ticket_ids_lst) > 0:
			ticket_ids_query='( '+" OR ".join(ticket_ids_lst)+' )'
			self.queries.append(ticket_ids_query)

		# Priorities
		prio_matrix=[(self.p1_check,"1-Critical"),(self.p2_check,"2-High"),(self.p3_check,"3-Medium"),(self.p4_check,"4-Low")]
		prio_statement='\'Priority*\' = '
		self.build_query(prio_matrix,prio_statement)

		# Status
		stat_matrix=[(self.sA_check,"Assigned"),(self.sI_check,"In Progress"),(self.sP_check,"Pending"),(self.sR_check,"Resolved"),(self.sC_check,"Clsoed"),(self.sN_check,"Cancelled")]
		stat_statement='\'Status*\' = '
		self.build_query(stat_matrix,stat_statement)

		# Type
		type_matrix=[(self.tINC_check,"Incident"),(self.tSR_check,"Service Request")]
		type_statement='\'Incident Type*\' = '
		self.build_query(type_matrix,type_statement)

		# Mont/Cust
		mc_query="(\'Reported Source\' = \"Monitoring - E2E\" OR \'Reported Source\' = \"Monitoring - Email Interface\" OR \'Reported Source\' = \"Monitoring - HPOVO - automatically\" OR \'Reported Source\' = \"Monitoring - HPOVO - manually created\" OR \'Reported Source\' = \"Monitoring - HPOVO - manually triggered\")"
		if self.mcMONT_check.get_active() and self.mcCUST_check.get_active():
			pass	
		elif self.mcMONT_check.get_active():
			self.queries.append(mc_query)
		elif self.mcCUST_check.get_active():
			self.queries.append("( 'Reported Source' = NULL OR NOT "+mc_query+" )")

		# SLA Status
		sla_matrix=[(self.slaMet_check,"Within the Service Target"),(self.slaWar_check,"Service Target Warning"),(self.slaBre_check,"Service Targets Breached"),(self.slaNon_check,"NULL")]
		sla_statement='\'SLM Real Time Status\' = '
		self.build_query(sla_matrix,sla_statement)

		# Service
		srv_matrix=[(self.service_check[i[0]],i[1]) for i in self.service_list]
		srv_statement='\'Product Categorization Tier 3\' = '
		self.build_query(srv_matrix,srv_statement)

		# Assigned Group 
		groups=[]
		for team in self.teams_list:
			if self.teams_check[team[0]].get_active():
				groups+=team[1]
		
		if self.ag_all.get_active():
			pass
		else:
			q_groups=[]
			for group in groups:
				q_groups.append('\'Assigned Group*+\' = '+'\"'+group+'\"')
			query_txt='( '+" OR ".join(q_groups)+' )'
			self.queries.append(query_txt)

		# Company
		c_matrix=[(self.company_check[i[0]],i[1]) for i in self.company_list]
		c_statement='\'Company*+\' = '
		self.build_query(c_matrix,c_statement)

		# Submit Date
		subd_matrix=[(self.subd_start_check,self.subd_start_entry),(self.subd_end_check,self.subd_end_entry)]
		subd_statement='\'Submit Date\''
		self.build_date_query(subd_matrix,subd_statement)

		# Modified Date
		modd_matrix=[(self.modd_start_check,self.modd_start_entry),(self.modd_end_check,self.modd_end_entry)]
		modd_statement='\'Last Modified Date\''
		self.build_date_query(modd_matrix,modd_statement)

		# Resolved Date
		resd_matrix=[(self.resd_start_check,self.resd_start_entry),(self.resd_end_check,self.resd_end_entry)]
		resd_statement='\'Last Resolved Date\''
		self.build_date_query(resd_matrix,resd_statement)
		
		#print ticket_ids_lst
		final_query=" AND ".join(self.queries)
		self.query.set_text(final_query)

		# if self.automatic_copy_check active copy to clipbaord
		if self.automatic_copy_check.get_active(): 
			self.clipboard.set_text(final_query, -1)

	# function to build the query, it takes a list of tuple (checkbutton_name,value) and used statement
	def build_query(self,matrix,statement):
		query=[]
		active=[ i[0].get_active() for i in matrix ]
		if not all(active):
			for i in matrix:
				if i[0].get_active():
					if i[1] == "NULL":
						query.append(statement+i[1])
					else:
						query.append(statement+"\""+i[1]+"\"")
			query_txt='( '+" OR ".join(query)+' )'
			self.queries.append(query_txt)

	# function to build the query for Submit/Modified/Resolved date
	def build_date_query(self,matrix,statement):
		query=[]
		if matrix[0][0].get_active() or matrix[1][0].get_active():
			if matrix[0][0].get_active():
				query.append(statement+' >= \"'+matrix[0][1].get_text()+'\"')
			if matrix[1][0].get_active():
				query.append(statement+' <= \"'+matrix[1][1].get_text()+'\"')
			query_txt='( '+" AND ".join(query)+' )'
			self.queries.append(query_txt)

	# Function to quit
	def quit(self,widget):
		Gtk.main_quit()

	# function to reset to initial state
	def reset(self,widget):
		self.ticket_ids.get_buffer().set_text("")
		self.query.set_text("")
		for i in self.check_container:
			i.set_active(True)
		for i in [self.subd_start_check,self.subd_end_check,self.modd_start_check,self.modd_end_check,self.resd_start_check,self.resd_end_check]:
			i.set_active(False)

	# Function to display the About dialog
	def about(self,widget):
		self.about_win = self.builder.get_object("about_window")
		self.about_win.connect("response", self.on_close)
		self.about_win.show()

	# Function to hide the about Dialog
	def on_close(self, action, parameter):
		action.hide()
		


	
if __name__ == "__main__":
	q=query_builder()
