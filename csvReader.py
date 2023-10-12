def csvReader():
    import csv
    from ipaddress import IPv4Network, IPv6Network
    
    # Create variables.
    logAddThis = str()          # String: Written to a log file, which is
                                # overwritten each time that this script
                                # runs.  Used to review output.
    csvImportedData = list()    # List variable: Imported CSV information.
    ipNetworksSorted = dict()   # Dictionary variable - The keys are parent 
                                # networks; values are subnets within the
                                # scope of the key (parent network) and are
                                # stored as a list variable.
    ipNetworksOutput = dict()   # Final output
    netMembershipCheck = list() # List variable: Network keys without members.
                                # This script will iterate through these to see
                                # if they are counted as a member network.
    netZeroNonMembers = list()  # Explanation comes later

                                    
    # Open the file and iterate though it, line by line. Format 'keyName' as an
    # IPv4 network.  The format of the file 'rawipv4.csv' should have two
    # columns: the first column is the network address, and the second is the
    # subnet.  These should be separated by a comma.
    
    with open('rawipv4.csv', 'r') as csvFile:
    # with open('rawipv6.csv', 'r') as csvFile:
        csvFileData = csv.reader(csvFile, delimiter = ',')
        for thisLine in csvFileData:
            keyName = thisLine[0] + '/' + thisLine[1]   # network + CIDR
            csvImportedData.append(keyName)
    
    # Populate keys for dictionary variable 'ipNetworksSorted'; set values to
    # be list variables.  These will be populated later.
    for thisNetwork in csvImportedData:
        ipNetworksSorted[thisNetwork] = list()

    # Populate values for keys in 'ipNetworksSorted'; keys should not appear in
    # their own list of values.  If item 'thisNetwork' is not the key
    # 'keyNetwork' AND a subnet of keyNetwork, it will be added to keyNetwork's
    # list of values.
    for keyNetwork in ipNetworksSorted.keys():
        for thisNetwork in csvImportedData:
            #if IPv4Network(thisNetwork) != IPv4Network(keyNetwork):                 # Remove duplicates.
                #if IPv4Network(thisNetwork).subnet_of(IPv4Network(keyNetwork)):
                    #ipNetworksSorted[keyNetwork].append(thisNetwork)
            if IPv6Network(thisNetwork) != IPv6Network(keyNetwork):                 # Remove duplicates.
                if IPv6Network(thisNetwork).subnet_of(IPv6Network(keyNetwork)):
                    ipNetworksSorted[keyNetwork].append(thisNetwork)

    # Iterate through 'ipNetworksSorted' again; populate keys with values into
    # the dictionary variable 'ipNetworksOutput'.  Keys with zero-length values
    # will be added to list variable 'netMembershipCheck' for additional
    # evaluation.
    for networkParent, networkMembers in ipNetworksSorted.items():
        if len(networkMembers) != 0:
            ipNetworksOutput[networkParent] = networkMembers
        elif len(networkMembers) == 0:
            netMembershipCheck.append(networkParent)

    ipNO = str(ipNetworksOutput.values())
    for netMC in netMembershipCheck:
        if netMC not in ipNO:
            netZeroNonMembers.append(netMC)

    # Logging
    logAddThis += 'The following networks have no overlap:\n'
    for nznm in netZeroNonMembers:
        logAddThis += nznm + ', '

    for networkParent, networkMembers in ipNetworksOutput.items():
        logAddThis += '\n\nNetwork ' + networkParent + ' overlaps the following networks:\n'
        logAddThis += str(networkMembers)

    log = open('IPv4_LogFile.txt', 'w')
    # log = open('IPv6_LogFile.txt', 'w')
    log.write(logAddThis)
    log.close()
    exit()

csvReader()