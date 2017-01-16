import random
import shutil

class Quotes:
    """
    Quotes handler class.
    """

    def __init__(self, quotesfile):
        """
        Initialize the quotes, saving the quotes file location.
        """
        self.db = quotesfile
        self.bak = 'backup.db'

    def num_of_quotes(self):
        """
        The total number of quotes.

        Returns:
            The number of quotes.
        """
        num_lines = 0
        with open(self.db, "r") as myfile:
            num_lines = sum(1 for line in myfile)

        return num_lines

    def save(self, text):
        """
        Save a quote in the quotes file.

        Args:
            text(str): The quote to save.

        Raises:
            ValueError: if quote text is empty or None.
        """
        if not text:
            raise ValueError('Quote text can\'t be null or empty.')

        with open(self.db, "a") as myfile:
            myfile.write(text+'\n')

    def remove(self, num):
        """
        Remove a quote in the quotes file.

        Args:
            num(int): The quote id.

        Raises:
            ValueError: if quote text is empty or None.
        """
        if num < 1 or num > self.num_of_quotes():
            raise ValueError('Quote number is out of range')
        
        # cleanup backup file
        open(self.bak, 'w').close()

        # write backup file
        with open(self.db, 'r') as myfile:
            with open(self.bak, 'r+') as bakfile:
                for i, line in enumerate(myfile):
                    if i != num - 1:
                        bakfile.write(line)

        # override current db
        shutil.copyfile(self.bak, self.db)

    def read(self, num):
        """
        Read a quote corresponding to its number.

        Args:
            num(int): The number of the quote to read.

        Raises:
            ValueError: if quote text is empty or None.

        Returns:
            str: The quote text. If None, no quote has been found.
        """
        if num < 1 or num > self.num_of_quotes():
            raise ValueError('Quote number is out of range')
        
        text = None

        with open(self.db, "r") as myfile:
            for i, line in enumerate(myfile):
                if i == num - 1:
                    text = line
                    
        return text

    def random_read(self):
        """
        Read a random quote from the quotes file.

        Returns:
            str: The quote text. If None, no quote has been found.
            int: The index of the quote.
        """
        num_lines = self.num_of_quotes()
        if num_lines == 0:
            return None

        num = random.randint(1, num_lines)
        text = self.read(num)

        return text, num
