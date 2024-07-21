from time import sleep
from smartcard.util import toHexString
from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver
from smartcard.System import readers

class printobserver(ReaderObserver):
    """A simple reader observer that is notified
    when readers are added/removed from the system and
    prints the list of readers
    """

    def update(self, observable, actions):
        (addedreaders, removedreaders) = actions
        print("Added readers", addedreaders)
        print("Removed readers", removedreaders)
        # Use the first available reader
        reader = addedreaders[0]
        # List available readers
        available_readers = readers()
        print("Available readers:", available_readers)

        if not available_readers:
            print("No readers found.")
            exit()
        connection = reader.createConnection()
        connection.connect()
        print("Reader:", reader)
        print("Card ATR:", toHexString(connection.getATR()))

if __name__ == '__main__':
    print("Add or remove a smartcard reader to the system.")
    print("This program will exit in 10 seconds")
    print("")
    readermonitor = ReaderMonitor()
    readerobserver = printobserver()
    readermonitor.addObserver(readerobserver)

    sleep(10)

    # don't forget to remove observer, or the
    # monitor will poll forever...
    readermonitor.deleteObserver(readerobserver)