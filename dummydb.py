authors = [
    {
        'id':1,                     # pk
        #'first_name':'tite',
        #'last_name':'kuba',
        'name':'Tite Kubo',         # name should actually be stord as two attributes
        'email':'kubo@example.com', # unique not null
        'pen_name':'Tite Kubo'      # not null
    }
]

stories = [
    {
        'id':1,             # pk
        'author_id':1,      # fk, not null
        'name':'Bleach',    # not null
        'status':'Ongoing',
        'description':"Bleach (stylized as BLEACH) is a Japanese manga series written and illustrated by Tite Kubo. It follows the adventures of a teenager Ichigo Kurosaki, who inherits his parents' destiny after he obtains the powers of a Soul Reaper—a death personification similar to the Grim Reaper—from another Soul Reaper, Rukia Kuchiki."
    },
]

arcs = [
    {
        'id':1,
        'story_id':1,
        'name':'Soul Society Arc',
        'description':'Ichigo goes to soul society, beats up Byakuya, gets thoroughly beat up by Aizen'
    },
    {
        'id':2,
        'story_id':1,
        'name':'Huecomundo Arc',
        'description':'Ichigo goes to Huecomundo, beats up a bunch of Espada'
    },
]

characters = [
    {
        'id':1,
        'author_id':1,
        'name':'Shigekuni Genryuusai Yamamoto',
        'race_id':3,
        'gender':'Male',
        'status':'Deceased',
        'height':None,
        'weight':None,
        'age':2000,
        'alignment':'Lawful-Good',
        'description':'The Captain Commander of the 13 Court Guard Squads, the oldest and stronget of the Soul Reapers.'
    },
    {
        'id':2,
        'author_id':1,
        'name':'Ichigo Kurosaki',
        'race_id':1,
        'gender':'Male',
        'status':'Alive',
        'height':None,
        'weight':None,
        'age':17,
        'alignment':'Lawful-Good',
        'description':"You know who Ichigo is, I'm not gonna type all that."
    },
]

traits = [
    
]

worlds = [
    {
        'id':1,
        'author_id':1,
        'name':'World of the Living',
        'description':'Modern day earth.'
    },
    {
        'id':2,
        'author_id':1,
        'name':'Huecomundo',
        'description':'A desolate wasteland which the hollows call home.'
    },
    {
        'id':3,
        'author_id':1,
        'name':'Soul Society',
        'description':'Where the souls of the dead, and the soul reapers reside.'
    },
]

locations = [
    {
        'id':1,
        'author_id':1,
        'world_id':1,
        'location_id':None,
        'category':'Town',
        'name':'Karakura Town',
        'description':'The town where Ichigo lives.'
    },
    {
        'id':2,
        'author_id':1,
        'world_id':1,
        'location_id':1,
        'category':'School',
        'name':'Karakura School',
        'description':'The school Ichigo goes to.'
    },
    {
        'id':3,
        'author_id':1,
        'world_id':3,
        'location_id':None,
        'category':'City',
        'name':'Sereitei',
        'description':'The home of the Soul Reapers.'
    },
]

races = [
    {
        'id':1,
        'author_id':1,
        'name':'Human',
        'category':'Human',
        'description':'Normal humans, no different from the humanity of our world.'
    },
    {
        'id':2,
        'author_id':1,
        'name':'Hollow',
        'category':'Monster',
        'description':'Lost souls with lingering regrets that were unable to move on.'
    },
    {
        'id':3,
        'author_id':1,
        'name':'Soul Reaper',
        'category':'Human',
        'description':'Responsible for maintaining the balance of souls in the three realms.'
    },
]

items = [
    {
        'id':1,
        'author_id':1,
        'name':'Excalibur',
        'rarity':'Legendary',
        'category':'Weapon',
        'description':'The mythical sword of King Arthur.'
    },
    {
        'id':2,
        'author_id':1,
        'name':'Health Potion',
        'rarity':'Common',
        'category':'Consumable',
        'description':'Common item easily accessible to most people.'
    },
    {
        'id':3,
        'author_id':1,
        'name':'Zangetsu',
        'rarity':'Unique',
        'category':'Weapon',
        'description':"Ichigo Kurosaki's Zanpakuto"
    },
    {
        'id':4,
        'author_id':1,
        'name':'Zanpakuto',
        'rarity':'Rare',
        'category':'Weapon',
        'description':'The weapon of the Soul Reapers. It is unique for every soul reaper.'
    },
]

organizations = [
    {
        'id':1,
        'author_id':1,
        'leader_id':1,
        'base_location_id':1,
        'name': '13 Court Guard Squads',
        'description':'The guardians of Soul Society. They reside in the Sereitei and maintain the baance of Souls between the World of the Living and Soul Society',
    },
]

character_appears_in = [
    {
        'character_id':1,
        'arc_id':1,
        'role':'Minor Antagonist',
        'role_description': "Yamamoto is the pillar of Soul Society. When Ichigo and friends attack, he gives the command to hunt them down. But he ultimately plays no significant role"
    },
    {
        'character_id':2,
        'arc_id':1,
        'role':'Protagonist',
        'role_description': 'Ichigo and Friends invade the Soul Society to save Rukia.'
    },
]

item_featured_in = [
    {
        'item_id':3,
        'arc_id':1,
    }
]

arc_occurs_in = [
    {
        'arc_id':1,
        'location_id':3,
    },
    {
        'arc_id':2,
        'location_id':2,
    }
]

race_lives_in = [
    {
        'race_id':1,
        'world_id':1,
    },
    {
        'race_id':2,
        'world_id':2,
    },
    {
        'race_id':3,
        'world_id':3,
    },
    {
        'race_id':2,
        'world_id':1,
    }
]

item_found_in_world = [
    {
        'item_id':4,
        'world_id':3,
    }
]

# ignore this
mapper = {
    'author':authors,
    'story':stories,
    'arc':arcs,
    'world':worlds,
    'characters':characters,
    'traits':traits,
    'location':locations,
    'race':races,
    'item':items,
    'item_featured_in':item_featured_in,
    'appearance':character_appears_in,
    'race_lives_in':race_lives_in,
    'arc_occurs_in':arc_occurs_in,
    'item_found_in_world':item_found_in_world,
    'organization':organizations,
}

def get_columns(_from):
    table = mapper[_from]
    columns = []
    for key in table[0].keys():
        columns.append({'COLUMN_NAME':key})
    return columns

def query(_from, _col, _val, _aslist=True):
    res = []
    print(_from, _col, _val)
    try:
        for item in mapper[_from]:
            flag = True
            for i in range(len(_col)):
                if _val[i] != item[_col[i]]:
                    flag = False
                    break
            if flag:
                if not _aslist:
                    return item
                res.append(item)
    except Exception as e:
        print(e)

    if _aslist:
        return res
    return None

def join(listA, listB):
    res = [{} for i in range(len(listA))]
    for i in range(len(res)):
        for key in listA[i].keys():
            res[i][key] = listA[i][key]
        for key in listB[i].keys():
            res[i][key] = listB[i][key]
    return res

def insert(_to, _val):
    table = mapper[_to]
    temp = {}
    for _key in table[0].keys():
        if _key in _val:
            temp[_key] = _val[_key]
        else:
            temp[_key] = None
    temp['id'] = len(table) + 1
    table.append(temp)