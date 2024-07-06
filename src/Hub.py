import zmq


class Publisher:
    def __init__(self,node,topics,address,port):
        self.topics = topics
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
                self.registerPublisher(node = message['node'],topics = message['topics'],address=message['address'])
            else:
                #print('hellow')
                self.registerSubscription(node=message['node'],topic=message['topic'])
            #print([vars(publisher) for publisher in self.publishers])
            
    def registerPublisher(self,node,topics,address):
        publisher = Publisher(node,topics,address,self.next_port)
        self.next_port +=1
        self.publishers.append(publisher)
        self.socket.send_json({'status': 'success', 'data': vars(publisher)})

    def registerSubscription(self,node,topic):
        publishers = [publisher for publisher in self.publishers if publisher.node==node ]
        if len(publishers) == 0:
            return self.socket.send_json({'status': 'fail'})
        if len(publishers)>1:
            raise Exception('there should be no more than one publisher for a node')
        publisher = publishers[0]
        if not topic in publisher.topics:
            raise Exception(f'no topic {topic} was found')
        self.socket.send_json({'status': 'success', 'data': vars(publisher)})




