from GT import GT_Excel_Interface, GT_ACB35_Settings, GT_Repository

def main():
    new_test = GT_Excel_Interface.Test_File("Write", "Test_File")
    new_test.name_file("Test_File.xlsx")
    repos = GT_Repository.Repository()

    repos.setup("35")
    repos.set_mapping_dictionary()

    new_test.write_cell(1,1,0,"Main")
    new_test.write_cell(2,2,0,"Configuration")
    new_test.write_cell(2,3,0,"Family")
    new_test.write_cell(2,4,0,"Frame")
    new_test.write_cell(2,5,0,"Rating")
    new_test.write_cell(2,3,0,"ACB")
    new_test.write_cell(2,4,0,"Standard")
    new_test.write_cell(2,5,0,"1000")
    
    
    new_test.write_cell(5,2,0,"Important Info")
    

    i = 0 
    for key in repos.mapping_dictionary:
        if "Buffer" in key:
            pass
        elif "Main" in key:
            pass
        elif "pf" in key:
            pass
        elif 'Inputs' in key:
            i = i+1
            new_test.create_tab(key)
            my_array = repos.mapping_dictionary[key][0]
            
            new_test.write_row_with_array(1,1,i, my_array)
            j = 1
            for etu_key in my_array:
                val = repos.expected[etu_key]
                print(val)
                new_test.write_cell(j,2,i,val)
                j = j+1
        else:
            new_test.create_tab(key)
            my_array = repos.mapping_dictionary[key][0]

            i = i+1
            new_test.write_cell(1,1,i,key)
            new_test.write_row_with_array(1,4,i, my_array)

            j = 1
            for etu_key in my_array:
                val = repos.etu_dictionary[etu_key][0]
                new_test.write_cell(j,5,i,val)
                j = j+1
                
    new_test.save_file()
        

    
main()
