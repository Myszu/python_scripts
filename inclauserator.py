from time import sleep

class Inclauserator():
    def __init__(self) -> None:
        # Number of characters in one "IN" clause
        self.in_limit = 10000
        
        # Number of characters in whole statement before spliting to multiple queries
        self.out_limit = 120000
        
        # Name of the column
        self.column_name = 'NAME'
        
        # Source data in form of list of items (seperated with new lines)
        self.source_data = """ REPLACE ME WITH THE LIST
""".split()
    
    
    def run(self) -> None:
        if not self.column_name or not self.source_data: return
        self.source_data = [f"'{element}'" for element in self.source_data]
        rows = ''
        iteration = ''
        capsule = ''
        files = 0
        
        for i in range(0, len(self.source_data), 10):
            row = ','.join([elements for elements in self.source_data[(0+i):(0+(i+10))]]) if not rows else ',\n' + ','.join([elements for elements in self.source_data[(0+i):(0+(i+10))]])
            
            if len(row) + len(rows) < self.in_limit:
                rows += row
            else:
                if not capsule:
                    iteration = f"""{self.column_name} IN (
                    {rows}
                    )
                    """
                else:
                    iteration = f"""OR {self.column_name} IN (
                    {rows}
                    )
                    """
                if len(capsule) + len(iteration) < self.out_limit:
                    capsule += iteration
                else:
                    if iteration[0:3] == "OR ": iteration = iteration.replace("OR ", "", 1)
                    f = open(f"clause-{files}.txt", "w")
                    f.write(capsule)
                    f.close()
                    files += 1
                    capsule = '' + iteration
                rows = ','.join([elements for elements in self.source_data[(0+i):(0+(i+10))]])
        if not capsule:
            iteration = f"""{self.column_name} IN (
            {rows}
            )
            """
        else:
            iteration = f"""OR {self.column_name} IN (
            {rows}
            )
            """
        capsule += iteration
        if files:
            if iteration[0:3] == "OR ": iteration = iteration.replace("OR ", "", 1)
            f = open(f"clause-{files}.txt", "w")
            f.write(capsule)
            f.close()
        else:
            f = open("clause.txt", "w")
            f.write(capsule)
            f.close()
        files += 1
        
        print(f'All done! Generated clauses in {files} files to avoid reaching {self.out_limit} characters limit.')
        sleep(0.5)
        for i in range(5,0,-1):
            print(f'Closing script in {i}', end='\r')
            sleep(1)


if __name__ == '__main__':
    inclauserator = Inclauserator()
    inclauserator.run()