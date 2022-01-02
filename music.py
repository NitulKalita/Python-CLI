from earsketch import *

init()
setTempo(120)

sounds = [0,0,0,0,0,0]

sounds[0] = EIGHT_BIT_ATARI_LEAD_003
sounds[1] = RD_TRAP_MAIN808_BEAT_5
sounds[2] = HIPHOP_FUNKBEAT_005
sounds[3] = RD_UK_HOUSE__SFX_PERC_1
sounds[4] = EIGHT_BIT_ATARI_LEAD_001
sounds[5] = EIGHT_BIT_ATARI_LEAD_009

fitMedia(sounds[0],1,1,3)
fitMedia(sounds[1],2,3,50)
fitMedia(sounds[2],3,8,50)
fitMedia(sounds[3],4,10,50)
fitMedia(sounds[4],5,20,28)
fitMedia(sounds[5],6,31,38)

finish()