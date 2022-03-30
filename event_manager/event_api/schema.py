import graphene
from graphene import relay, ObjectType
from .models import Event
from django.core.exceptions import ObjectDoesNotExist
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


############# TYPY #############
class EventType(DjangoObjectType):
    class Meta:
        model = Event
        filter_fields = {'name': ['iexact', 'icontains', 'istartswith', 'iendswith'],
                         'uuid': ['iexact', 'icontains', 'istartswith', 'iendswith'],
                         'source': ['iexact', 'icontains', 'istartswith', 'iendswith'],
                         'created_at': ['iexact', 'icontains', 'istartswith', 'iendswith'],
                         'updated_at': ['iexact', 'icontains', 'istartswith', 'iendswith'],
                         'description': ['iexact', 'icontains', 'istartswith', 'iendswith'],
                         }
        interfaces = (relay.Node, )


    

############# QUERY #############
class Query(ObjectType): 
    all_events = graphene.List(EventType)  
    event_by_uuid = graphene.Field(EventType, uuid=graphene.String())
    filter_all_events = DjangoFilterConnectionField(EventType)
    # wszystkie eventy
    def resolve_all_events(root, info):
        return Event.objects.all()
    
    # event o konkretnym UUID
    def resolve_event_by_uuid(root, info, uuid):
        try:
            event = Event.objects.get(uuid=uuid)
            return event
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Event with UUID='{uuid}' does not exist!")
        
    # filtrowanie po nazwie
    

############# MUTACJE #############
# tworzenie nowego eventu
class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)
        source = graphene.String(required=True)
        description = graphene.String(required=True)
    event = graphene.Field(EventType) 
    
    @classmethod
    def mutate(cls, root, info, name, source, description):
        event = Event(name=name, source=source, description=description)   
        event.save() 
        return CreateEvent(event=event)


 # usuwanie eventu o konkretnym UUID   
class DeleteEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID()
    event = graphene.Field(EventType)
    
    @classmethod
    def mutate(cls, root, info, uuid):
        event = Event.objects.get(uuid = uuid)
        event.delete()
        return DeleteEvent(event=event)
 
 
# update wszystkich edytowalnych pól (name, source, description) eventu o konkretnym UUID
class UpdateEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID()
        name = graphene.String()
        source = graphene.String()
        description = graphene.String()
    event = graphene.Field(EventType) 
    
    @classmethod
    def mutate(cls, root, info,uuid, name, source, description):
        try:
            event = Event.objects.get(uuid=uuid)
            event.source = source
            event.name = name
            event.description = description
            event.save() 
            return UpdateEvent(event=event)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Event with UUID='{uuid}' does not exist!")
    
    
# update 'name' eventu o konkretnym UUID
class UpdateEventName(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        uuid = graphene.UUID()
    event = graphene.Field(EventType) 
    
    @classmethod
    def mutate(cls, root, info,uuid, name):
        try:
            event = Event.objects.get(uuid=uuid)
            event.name = name
            event.save() 
            return UpdateEventName(event=event)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Event with UUID='{uuid}' does not exist!")


# pdate 'source' eventu o konkretnym UUID    
class UpdateEventSource(graphene.Mutation):
    class Arguments:
        source = graphene.String()
        uuid = graphene.UUID()
    event = graphene.Field(EventType) 
    
    @classmethod
    def mutate(cls, root, info,uuid, source):
        try:
            event = Event.objects.get(uuid=uuid)
            event.source = source
            event.save() 
            return UpdateEventSource(event=event)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Event with UUID='{uuid}' does not exist!")
 
 
# update 'description' eventu o konkretnym UUID   
class UpdateEventDescription(graphene.Mutation):
    class Arguments:
        description = graphene.String()
        uuid = graphene.UUID()
    event = graphene.Field(EventType) 
    
    @classmethod
    def mutate(cls, root, info,uuid, description):
        try:
            event = Event.objects.get(uuid=uuid)
            event.name = description
            event.save() 
            return UpdateEventDescription(event=event)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Event with UUID='{uuid}' does not exist!")
 
 
 
 # usuwanie eventu o konkretnym UUID   
class DeleteEvent(graphene.Mutation):
    class Arguments:
        uuid = graphene.UUID()
    event = graphene.Field(EventType)
    
    @classmethod
    def mutate(cls, root, info, uuid):
        try:
            event = Event.objects.get(uuid = uuid)
            event.delete()
            return DeleteEvent(event=event)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Event with UUID='{uuid}' does not exist!")

    

# wszystkie mutacje
class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    delete_event = DeleteEvent.Field()
    update_event = UpdateEvent.Field()
    update_event_name = UpdateEventName.Field()
    update_event_source = UpdateEventSource.Field()
    update_event_description = UpdateEventDescription.Field()
   
   
############# SCHEMA #############     
schema = graphene.Schema(query=Query, mutation=Mutation)
