from time import sleep
import combat

SCRIPT_NAME = "HASKEL_PAXTON_CONVERSATION"


def script(subzone, character):
    print("*" * 40)
    print("Brother Haskel says: Everything is going according to plan, \
    I have set you up a meeting with the Archbishop in three weeks.")
    sleep(3)
    print("Brother Paxton says: It will be an honor for me.")
    sleep(2.5)
    print("Brother Haskel says: All these years have led to this, you have better be prepared, Pax.")
    sleep(3)
    print("Brother Paxton says: I did not spend ten years in Ravenholdt for nothing.\
     Benedictus' end will bring forth a massive expedition to avenge him, \
     I only fear if the Brotherhood will be able to withstand it.")
    sleep(4)
    print(
        "Brother Haskel says: I have complete trust in Edwin's plans. \
        Your sacrifice will play a key role in our mission and for that you have my respect.")
    sleep(3)
    print("{char_name} says: Unbelievable, the two of you work for the Defias?!".format(char_name=character.name))
    sleep(2.5)

    # engage combat with Paxton
    brother_paxton = subzone._alive_monsters[subzone.GUID_BROTHER_PAXTON]
    combat.engage_combat(character, brother_paxton, subzone._alive_monsters, subzone._monster_guid_name_set,
                         subzone.GUID_BROTHER_PAXTON)

    print("Brother Haskel says: You have not seen the last of the Brotherhood, {char_name}!".format(
        char_name=character.name))
    sleep(2)
    print("Haskel drops a smoke bomb!")
    sleep(0.5)
    print("Smoke fills the hut...")
    sleep(2)
    print("When the smoke clears, you see that the traitor is nowhere in sight...")
    print()

    # remove Haskel because he escapes with a smoke bomb
    del subzone._alive_monsters[subzone.GUID_BROTHER_HASKEL]
    subzone._monster_guid_name_set.remove((subzone.GUID_BROTHER_HASKEL, "Brother Haskel"))