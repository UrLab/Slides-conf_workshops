""""
Name : Juliette C
date : 03 November 2024
Program : python script to write an WAV file 
    with one channel, sample rate at 44.1 kHz and 16bps
    
to do : 
if no PCM, function subChunkList to complete
"""

def returnByte(number : int, nbByte : int, isNegative : bool = False) -> bytes:
    """ return number in little endian on nbByte """
    return (number).to_bytes(nbByte, 'little', signed=isNegative)


def soundDataList() -> list[bytes]:
    """ create list of bytes for soundData """
    isUp, res = True, []

    for i in range(0, 44100):
        if ( i % 100 == 0) :
            isUp = (not isUp)
        sampleValue = 16383 if isUp else -16383
        res.append( returnByte(sampleValue, 2, not(isUp)) )

    return res


def dataChunkList() -> list[bytes]:
    """ return dataChunk for the WAV file"""
    soundData = soundDataList() 
    return [ b'data',
          returnByte( len(soundData) * 2, 4)] + soundData


def subChunkList(PCM : bool, nbChannels : int, sampleRate : int, bps : int) -> list[bytes]:
    """ return subChunk for the WAV file"""
    size = 16
    
    #only with PCM option on given
    if PCM :
        return [ b'fmt ',
                returnByte(size, 4),
                returnByte(1, 2), 
                returnByte(nbChannels, 2),
                returnByte(sampleRate, 4), 
                returnByte( sampleRate * nbChannels * bps // 8, 4),  # byte rate 
                returnByte( nbChannels * bps // 8, 2), # block align 
                returnByte( bps, 2) ]
    else :
        return None


def writeWavFile(path : str) -> None:
    """ write WAV file """
    
    if '.wav' not in path.split('/').pop():
        raise SyntaxError("no '.wav' extension in the path given")
    
    
    subChunk = subChunkList(True, 1, 44100, 16) 
    dataChunk = dataChunkList()

    bytesFile = [ b'RIFF', 
            returnByte( (len(dataChunk) - 2) * 2 + 36, 4),
            b'WAVE' ] + subChunk + dataChunk

    file = open(path, "wb") 

    for b in bytesFile :
        file.write(b)

    file.close()

path = 'outputPythonCode.wav'

writeWavFile(path)