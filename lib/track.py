# parser for song data
# player 1 is the game
# player 2 is the actual player
class Track:
    # do the thing
    def __init__(self, name):
        # opening file
        self.name = name
        self.path = "assets/tracks/" + name
        chartfile = open(self.path + "/chart.fnp", "r")
        chart = chartfile.read().split("\n")
        chartfile.close()

        # the header is the first line and contains stuff like the track name and bpm
        # format: NAME/BPM/SIGNATURE
        header = chart[0].split("/")
        self.displayname = header[0]
        self.bpm = float(header[1])
        self.signature = float(header[2])
        self.speed = int(header[3])
        self.damagemultiplier = float(header[4])
        self.length = len(chart) - 1
        self.beatlength = self.length * self.signature
        self.scene = "assets/scenes/" + header[5]
        self.p1 = header[6]
        self.p2 = header[7]

        # the rest of the file consists of note data
        # each line is one measure
        # format: PLAYER/BEAT/DIRECTION
        # special: 0/SPECIAL/PARAMETERS
        self.p1notes = []
        self.p2notes = []
        m = -1
        for measure in chart[1:]:
            m += 1
            for note in measure.split(" "):
                parameters = note.split("/")
                if parameters[0] == "1":
                    self.p1notes.append((
                        float(parameters[1]) + m * self.signature,
                        int(parameters[2])
                    ))
                elif parameters[0] == "2":
                    self.p2notes.append((
                        float(parameters[1]) + m * self.signature,
                        int(parameters[2])
                    ))
        
        print("p1 notes:", len(self.p1notes))
        print("p2 notes:", len(self.p2notes))
