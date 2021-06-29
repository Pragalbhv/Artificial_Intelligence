class bfhs(AlgorithmBase):
    # INITIAL INITIALISATION
    def execute(self):
        start=self.start_nodes[0]
        goal=self.goal_nodes[0]
        queue,visited=self.get_list('open'),self.get_list('closed')
#############################################################

        #DEFINING FUNCTIONS

        def setnodeval(node,g,h):# SETS VALUES FOR NODE
            self.set_node_attribute(node,'h',h)
            self.set_node_attribute(node,'g',g)
            self.set_node_attribute(node,'f',g+h)


        def propogate(node):#PATH RECONSTRUCTION
            
            gp=self.get_node_attribute(node,'g')
            for neighbor in self.neighbors(node):
                g=self.get_node_attribute(neighbor,'g')
                gnew=gp+self.get_edge_weight(node,neighbor)
                try:
                    if gnew< g:
                        setnodeval(neighbor,gnew,h)
                        self.set_parent(neighbor,node)
                        if neighbor in visited:
                            propogate(neighbor)
                except:
                    setnodeval(neighbor,gnew,h)
                    self.set_parent(neighbor,node)
                    if neighbor in visited:
                        propogate(neighbor)


        # The function is used for path reconstruction by Proogation
        #For each child of node, g is compared with its previous g value.
        #If previous g value does not exist then it directly assigns value.
        #recursion is used to reach all those affected






##################################### BEST FIRST SEARCH##########################################################################

        
        cost=border=2*self.heuristic(start,goal)#Assign initial value for U and cost of best first search path
        queue1=[]
        queue.append(start)
        queue1.append([start,self.heuristic(start,goal)])
#       queue1 is used that is sorted wrt the heuristic and then added to queue
#       sort wrt heuristic only 

        while queue:
            self.alg_iteration_start()
            node= queue.pop(0)
            rrrr=queue1.pop(0)
            visited.append(node)

            # GOAL CHECK
            if node==goal:
                visited.append(node)
                self.found_goal=True
                break

            for neighbor in self.neighbors(node):
#               children check
                if neighbor not in visited and neighbor not in queue:
#                     Assign parent and add [neighbor, heuristic] to queu1
                    queue1.append([neighbor,self.heuristic(neighbor,goal)])
                    self.set_parent(neighbor,node)
    
            queue1.sort(key = lambda x: x[1]) # sorting wrt heuristic
            queue.clear()
            #clear the queue to add according to heuristic from queue1
            for i in range(len(queue1)):
                queue.append(queue1[i][0])
        
        if self.found_goal:
            #if goal is found assign path cost to border [aka U, upper Bound]
            path=self.gen_path()
            # self.show_path(path)
            cost=0
            for i in range(len(path)-1):
                cost+=self.get_edge_weight(path[i],path[i+1])
            # print('cost by best first search',cost) for debugging 
            
        else: 
            self.show_info('No path available')

            
################################################################################################################################################
        #Clearing and prep for BFHS
        #Again setting heuristic values just in case.
        queue.clear()
        visited.clear()
        queue.append(start)
        border=cost
        self.set_node_attribute(start,'h',self.heuristic(start,goal))
        self.set_node_attribute(start,'g',0)
        self.set_node_attribute(start,'f',self.heuristic(start,goal))
###################################### BREADTH FIRST HEURISTIC SEARCH#############################################################

        while queue:
            self.alg_iteration_start()
            node= queue.pop(0)
            visited.append(node)

#           CHECK FOR GOAL
            if node==goal:
                visited.append(node)
                self.found_goal=True
                break
            for neighbor in self.neighbors(node):
#           ADDING CHILDREN FOR EACH NODE 
                h=g=oldg=0
                h=self.heuristic(neighbor,goal)
                g=self.get_node_attribute(node,'g')
                g=g+self.get_edge_weight(node,neighbor)
                if g+h <= border:
                    # ONLY IF h+g LESS THAN U WILL BE ADDED
                    if neighbor in queue:# neighbor in open, then check if new parent is better path
                        oldg= self.get_node_attribute(neighbor,'g')
                        if g< oldg:
                            setnodeval(neighbor,g,h)
                            self.set_parent(neighbor,node)
                    elif neighbor in visited:#      has children who will be affected
                        oldg= self.get_node_attribute(neighbor,'g')
                        if g< oldg:
                            setnodeval(neighbor,g,h)
                            self.set_parent(neighbor,node)
                            propogate(neighbor)
                            # reflect changes in g from new parent
                    else:
                        # simple add node
                        self.set_node_attribute(neighbor,'h',h)
                        self.set_node_attribute(neighbor,'g',g)
                        self.set_node_attribute(neighbor,'f',g+h)
                        self.set_parent(neighbor,node)
                        queue.append(neighbor)
                            



                    
            self.alg_iteration_end()






        if self.found_goal:
            # if goal found highlight path
            finalpath=self.gen_path()
            self.show_path(finalpath)
            finalcost=0
            for i in range(len(finalpath)-1):
                finalcost+=self.get_edge_weight(finalpath[i],finalpath[i+1])
            self.show_info('cost by BFHS:: '+str(finalcost))
            # print('heuristic', self.get_node_attribute(finalpath[0],'g')) same as above  used for debugging
            
        else: 
            self.show_info('No path available')



