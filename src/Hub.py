import zmq


class Publisher:
    def __init__(self,node,topic,address,port):
        self.topic = topic
        self.node = node
        self.address = address
        self.port = port
        self.full_address = f'{address}:{self.port}'

class Hub:
    def __init__(self):
        #self.publishers = [Publisher(node='camera',topic='frame',address='a',port='b')]
        self.publishers = []
        self.next_port = 5000
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        
    
    def run(self):
        self.socket.bind('tcp://*:3000')

        while True:
            message = self.socket.recv_json()
            print(message)
           
            if message['register_as'] == 'publisher':
                self.registerPublisher(node = message['node'],topic = message['topic'],address=message['address'])
            else:
                #print('hellow')
                self.registerSubscription(node=message['node'],topic=message['topic'])
            #print([vars(publisher) for publisher in self.publishers])
            
    def registerPublisher(self,node,topic,address):
        publisher = Publisher(node,topic,address,self.next_port)
        self.next_port +=1
        self.publishers.append(publisher)
        self.socket.send_json({'status': 'success', 'data': vars(publisher)})

    def registerSubscription(self,node,topic):
        publishers = [publisher for publisher in self.publishers if publisher.topic==topic and publisher.node==node ]
        print(publishers)
        if len(publishers)==0:
            return self.socket.send_json({'status': 'fail'})
        if len(publishers)>1:
            raise Exception('there should be no more than one publisher for node topic combo')
        publisher = publishers[0]
        self.socket.send_json({'status': 'success', 'data': vars(publisher)})




