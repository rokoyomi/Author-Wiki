author_list = [
    {
        'id':1,                     # pk
        #'first_name':'tite',
        #'last_name':'kuba',
        'name':'Tite Kubo',         # name should actually be stord as two attributes
        'email':'kubo@example.com', # unique not null
        'pen_name':'Tite Kubo'      # not null
    }
]

story_list = [
    {
        'id':1,             # pk
        'author_id':1,      # fk, not null
        'name':'Bleach',    # not null
        'description':"Bleach (stylized as BLEACH) is a Japanese manga series written and illustrated by Tite Kubo. It follows the adventures of a teenager Ichigo Kurosaki, who inherits his parents' destiny after he obtains the powers of a Soul Reaper—a death personification similar to the Grim Reaper—from another Soul Reaper, Rukia Kuchiki."
    },
]

story_genre_list = [
    {
        'story_id':1, # composite pk
        'genre_id':1  # composite pk
    },
]

genre_list = [
    {
        'id':1,             # pk
        'name':'Action',    # not null
    },
    {
        'id':2,
        'name':'Comedy',
    },
    {
        'id':2,
        'name':'Shounen',
    },
]

arc_list = [
    {
        'story_id':1,
        'name':'Soul Society Arc',
        'description':'Ichigo goes to soul society, beats up Byakuya, gets thoroughly beat up by Aizen'
    },
    {
        'story_id':1,
        'name':'Huecomundo Arc',
        'description':'Ichigo goes to Huecomundo, beats up a bunch of Espada'
    },
]

character_list = [
    {
        'id':1,
        'author_id':1,
        'name':'Mysterious Girl with a Book',
        'gender':'Female',
        'height':160,
        'weight':None,
        'age':None,
        'alignment':None,
        'description':'A mysterious girl sometimes seen in the labyrinth of knowledge, huddled in a corner and reading intently... '
    },
    {
        'id':2,
        'author_id':1,
        'name':'Ichigo Kurosaki',
        'gender':'Male',
        'height':None,
        'weight':None,
        'age':None,
        'alignment':None,
        'description':"You know who Ichigo is, I'm not gonna type all that."
    },
]

traits_list = [
    {
        'character_id':1,
        'name':'Personality',
        'description':'Unkown. All attempts at making contact have thus failed. The kid ignores everyone and anyone that attempts to get too close immediately collapses from "feelings of overwhelming dread".'
    },
    {
        'character_id':1,
        'name':'Appearance',
        'description':'She is short, looking to be in her early teens, with long blonde hair, and seemingly crimson red eyes--although no one has yet gotten near enough to be sure.'
    },
]

world_list = [
    {
        'id':1,
        'author_id':1,
        'name':'World of the Living',
        'description':'Where the living dwell'
    },
]

location_list = [
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
]

race_list = [
    {
        'id':1,
        'author_id':1,
        'name':'human',
        'description':'Standard humans, not much different from the humanity of our world.'
    },
]

item_list = [
    {
        'id':1,
        'author_id':1,
        'name':'Excalibur',
        'rarity':'legendary',
        'type':'weapon',
        'description':'The mythical sqord of King Arthur.'
    },
    {
        'id':2,
        'author_id':1,
        'name':'Health Potion',
        'rarity':'common',
        'type':'consumable',
        'description':'Common item easily accessible to most people.'
    },
    {
        'id':3,
        'author_id':1,
        'name':'Zangetsu',
        'rarity':'unique',
        'type':'weapon',
        'description':"Ichigo Kurosaki's Zanpakuto"
    },
    {
        'id':4,
        'author_id':1,
        'name':'Zanpakuto',
        'rarity':'rare',
        'type':'weapon',
        'description':'The weapon of the Soul Reapers. It is unique for every soul reaper.'
    },
]

appearance_list = [
    {
        'character_id':2,
        'story_id':1,
        'role':'Protagonist',
        'role_description': 'Ichigo is the primary main character of this story.'
    },
]

# ignore this
mapper = {
    'author':author_list,
    'story':story_list,
    'arc':arc_list,
    'world':world_list,
    'characters':character_list,
    'traits':traits_list,
    'location':location_list,
    'race':race_list,
    'item':item_list,
    'appearance':appearance_list,
    'genre':genre_list,
    'story_genre':story_genre_list,
}

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