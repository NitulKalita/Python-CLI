'''#using CLDR name
print("\N{grinning face}")
print("\N{winking face}")
print("\N{thumbs up sign}")
'''

'''#using unicodes
print("\U0001f600") #grinning face
print("\U0001F609") #winking face
print("\U0001F44D") #thumbs up
'''

#using the emoji module
import emoji

print(emoji.emojize(":grinning_face:"))
print(emoji.emojize(":winking_face:"))
print(emoji.emojize(":thumbs_up:"))