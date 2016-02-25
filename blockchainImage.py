# Experimental blockchain based files
# Usage:
#   python blockchainImage.py [image_name]
#
# Features:
#   Using blockchain API

from blockchain import blockexplorer
import base58
import time
import os
import sys

def deleteTmpFiles():
    os.remove('tmp58_1.txt')

def getTempFilesSize(filename):
    imageSize = str((os.stat(filename)).st_size)
    encoded58ImageSizeStepOne = str((os.stat('tmp58_1.txt')).st_size)
    print "The size of your image is: " + imageSize + " bytes"
    print "The size of the base58 encoded image is: " + encoded58ImageSizeStepOne + " bytes"

def createTmp58File(formattedSerialImage):
    tmpEncode = open('tmp58_1.txt', 'w')
    tmpEncode.write(formattedSerialImage)
    tmpEncode.close()

def turnIntoTransactions(latestBlockHeight, blocks, elementFromImage):
    print "Element received: " + str(elementFromImage)

    transactionsFromBlock = blocks[0].transactions
    transactionsNumber = len(transactionsFromBlock)
    for y in range(0, transactionsNumber):
        output = transactionsFromBlock[y].outputs
        addressFromOutput = str(output[0].address)
        indexFromTransaction = addressFromOutput.find(elementFromImage)
        if indexFromTransaction != -1:
            print "Section found on: " + addressFromOutput + " on block: " + str(latestBlockHeight) + " on transaction: " + str(y) + " on address position #" + str(indexFromTransaction)
            coded = [latestBlockHeight, y, indexFromTransaction]
            sys.exit()
            return coded

def compressionLab(encodedFile):
    fileReceived = encodedFile;
    byteSize = 4
    initLoop = 0
    endLoop = byteSize

    length = len(fileReceived) / byteSize
    print(length)

    blockchainCoordinates = [None] *  length
    latestBlockHeight = (blockexplorer.get_latest_block()).height

    for blockElement in range(latestBlockHeight, 0, -1):
        blocks = blockexplorer.get_block_height(blockElement)
        print(blockElement)
        for element in range(0, length):
            blockchainCoordinates[element] = turnIntoTransactions(latestBlockHeight, blocks, fileReceived[initLoop:endLoop])
            initLoop += byteSize
            endLoop += byteSize
            if endLoop >= len(fileReceived):
                initLoop = 0
                endLoop = byteSize

def base58encoding(filename, type):
    image = open(filename)
    serializedImage = base58.b58encode(image.read())
    createTmp58File(serializedImage)
    getTempFilesSize(filename)
    #base58decoding(serializedImage)
    return serializedImage

def base58decoding(serializedImage):
    image = open('backFrom58.jpg', 'w')
    unSerializedImage = base58.b58decode(serializedImage)
    image.write(unSerializedImage)
    image.close()

def suitableForEncoding(filename):
    if '.png' or '.jpg' or '.jpeg' in filename:
        return True
    else:
        return False

if __name__ == '__main__':
    filename = sys.argv[1]
    if suitableForEncoding(filename):
        if '.png' in filename:
            filetype = "PNG"
            encodedFile = base58encoding(filename, filetype)
            compressionLab(encodedFile)
            #base16encoding(filename, filetype)
        elif '.jpg'in filename:
            filetype = "JPG"
            encodedFile = base58encoding(filename, filetype)
            compressionLab(encodedFile)
            #base16encoding(filename, filetype)
        elif '.jpeg'in filename:
            filetype = "JPEG"
            base58encoding(filename, filetype)
            #base16encoding(filename, filetype)
