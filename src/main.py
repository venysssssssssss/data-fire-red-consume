import struct
import os
import sys
import binascii

# Dicionário de mapeamento de IDs de Pokémon para nomes
# IDs da 1ª geração (1-151) e da 3ª geração (252-386) para FireRed/LeafGreen
POKEMON_NAMES = {
    1: "Bulbasaur", 2: "Ivysaur", 3: "Venusaur", 4: "Charmander", 5: "Charmeleon", 
    6: "Charizard", 7: "Squirtle", 8: "Wartortle", 9: "Blastoise", 10: "Caterpie",
    11: "Metapod", 12: "Butterfree", 13: "Weedle", 14: "Kakuna", 15: "Beedrill",
    16: "Pidgey", 17: "Pidgeotto", 18: "Pidgeot", 19: "Rattata", 20: "Raticate",
    21: "Spearow", 22: "Fearow", 23: "Ekans", 24: "Arbok", 25: "Pikachu",
    26: "Raichu", 27: "Sandshrew", 28: "Sandslash", 29: "Nidoran♀", 30: "Nidorina",
    31: "Nidoqueen", 32: "Nidoran♂", 33: "Nidorino", 34: "Nidoking", 35: "Clefairy",
    36: "Clefable", 37: "Vulpix", 38: "Ninetales", 39: "Jigglypuff", 40: "Wigglytuff",
    41: "Zubat", 42: "Golbat", 43: "Oddish", 44: "Gloom", 45: "Vileplume",
    46: "Paras", 47: "Parasect", 48: "Venonat", 49: "Venomoth", 50: "Diglett",
    51: "Dugtrio", 52: "Meowth", 53: "Persian", 54: "Psyduck", 55: "Golduck",
    56: "Mankey", 57: "Primeape", 58: "Growlithe", 59: "Arcanine", 60: "Poliwag",
    61: "Poliwhirl", 62: "Poliwrath", 63: "Abra", 64: "Kadabra", 65: "Alakazam",
    66: "Machop", 67: "Machoke", 68: "Machamp", 69: "Bellsprout", 70: "Weepinbell",
    71: "Victreebel", 72: "Tentacool", 73: "Tentacruel", 74: "Geodude", 75: "Graveler",
    76: "Golem", 77: "Ponyta", 78: "Rapidash", 79: "Slowpoke", 80: "Slowbro",
    81: "Magnemite", 82: "Magneton", 83: "Farfetch'd", 84: "Doduo", 85: "Dodrio",
    86: "Seel", 87: "Dewgong", 88: "Grimer", 89: "Muk", 90: "Shellder",
    91: "Cloyster", 92: "Gastly", 93: "Haunter", 94: "Gengar", 95: "Onix",
    96: "Drowzee", 97: "Hypno", 98: "Krabby", 99: "Kingler", 100: "Voltorb",
    101: "Electrode", 102: "Exeggcute", 103: "Exeggutor", 104: "Cubone", 105: "Marowak",
    106: "Hitmonlee", 107: "Hitmonchan", 108: "Lickitung", 109: "Koffing", 110: "Weezing",
    111: "Rhyhorn", 112: "Rhydon", 113: "Chansey", 114: "Tangela", 115: "Kangaskhan",
    116: "Horsea", 117: "Seadra", 118: "Goldeen", 119: "Seaking", 120: "Staryu",
    121: "Starmie", 122: "Mr. Mime", 123: "Scyther", 124: "Jynx", 125: "Electabuzz",
    126: "Magmar", 127: "Pinsir", 128: "Tauros", 129: "Magikarp", 130: "Gyarados",
    131: "Lapras", 132: "Ditto", 133: "Eevee", 134: "Vaporeon", 135: "Jolteon",
    136: "Flareon", 137: "Porygon", 138: "Omanyte", 139: "Omastar", 140: "Kabuto",
    141: "Kabutops", 142: "Aerodactyl", 143: "Snorlax", 144: "Articuno", 145: "Zapdos",
    146: "Moltres", 147: "Dratini", 148: "Dragonair", 149: "Dragonite", 150: "Mewtwo",
    151: "Mew",
    # Adicionando alguns Pokémon da 2ª geração (152-251)
    152: "Chikorita", 153: "Bayleef", 154: "Meganium", 155: "Cyndaquil", 156: "Quilava",
    157: "Typhlosion", 158: "Totodile", 159: "Croconaw", 160: "Feraligatr",
    # Adicionando alguns Pokémon da 3ª geração (252-386)
    252: "Treecko", 253: "Grovyle", 254: "Sceptile", 255: "Torchic", 256: "Combusken",
    257: "Blaziken", 258: "Mudkip", 259: "Marshtomp", 260: "Swampert", 261: "Poochyena",
    262: "Mightyena", 263: "Zigzagoon", 264: "Linoone", 265: "Wurmple", 266: "Silcoon",
    267: "Beautifly", 268: "Cascoon", 269: "Dustox", 270: "Lotad", 271: "Lombre",
    272: "Ludicolo", 273: "Seedot", 274: "Nuzleaf", 275: "Shiftry", 276: "Taillow",
    277: "Swellow", 278: "Wingull", 279: "Pelipper", 280: "Ralts", 281: "Kirlia",
    282: "Gardevoir", 283: "Surskit", 284: "Masquerain", 285: "Shroomish", 286: "Breloom",
    287: "Slakoth", 288: "Vigoroth", 289: "Slaking", 290: "Nincada", 291: "Ninjask",
    292: "Shedinja", 293: "Whismur", 294: "Loudred", 295: "Exploud", 296: "Makuhita",
    297: "Hariyama", 298: "Azurill", 299: "Nosepass", 300: "Skitty",
    301: "Delcatty", 302: "Sableye", 303: "Mawile", 304: "Aron", 305: "Lairon",
    306: "Aggron", 307: "Meditite", 308: "Medicham", 309: "Electrike", 310: "Manectric",
    311: "Plusle", 312: "Minun", 313: "Volbeat", 314: "Illumise", 315: "Roselia",
    316: "Gulpin", 317: "Swalot", 318: "Carvanha", 319: "Sharpedo", 320: "Wailmer",
    321: "Wailord", 322: "Numel", 323: "Camerupt", 324: "Torkoal", 325: "Spoink",
    326: "Grumpig", 327: "Spinda", 328: "Trapinch", 329: "Vibrava", 330: "Flygon",
    331: "Cacnea", 332: "Cacturne", 333: "Swablu", 334: "Altaria", 335: "Zangoose",
    336: "Seviper", 337: "Lunatone", 338: "Solrock", 339: "Barboach", 340: "Whiscash",
    341: "Corphish", 342: "Crawdaunt", 343: "Baltoy", 344: "Claydol", 345: "Lileep",
    346: "Cradily", 347: "Anorith", 348: "Armaldo", 349: "Feebas", 350: "Milotic",
    351: "Castform", 352: "Kecleon", 353: "Shuppet", 354: "Banette", 355: "Duskull",
    356: "Dusclops", 357: "Tropius", 358: "Chimecho", 359: "Absol", 360: "Wynaut",
    361: "Snorunt", 362: "Glalie", 363: "Spheal", 364: "Sealeo", 365: "Walrein",
    366: "Clamperl", 367: "Huntail", 368: "Gorebyss", 369: "Relicanth", 370: "Luvdisc",
    371: "Bagon", 372: "Shelgon", 373: "Salamence", 374: "Beldum", 375: "Metang",
    376: "Metagross", 377: "Regirock", 378: "Regice", 379: "Registeel", 380: "Latias",
    381: "Latios", 382: "Kyogre", 383: "Groudon", 384: "Rayquaza", 385: "Jirachi",
    386: "Deoxys"
}

def get_pokemon_name(species_id):
    """Retorna o nome do Pokémon baseado no ID da espécie"""
    return POKEMON_NAMES.get(species_id, f"Desconhecido (ID: {species_id})")

def calculate_checksum(data):
    checksum = sum(struct.unpack_from('<2048H', data, 0)) & 0xFFFF
    return checksum

def verify_section(data, ignore_checksum=True):
    if len(data) < 4096:
        print("Seção inválida: tamanho menor que 4096 bytes")
        return False
    try:
        stored_checksum = struct.unpack_from('<H', data, 4094)[0]
        calculated = calculate_checksum(data)
        if calculated != stored_checksum:
            print(f"Checksum inválido: calculado={calculated:04X}, armazenado={stored_checksum:04X}")
        return ignore_checksum or (calculated == stored_checksum)
    except struct.error as e:
        print(f"Erro ao verificar checksum: {str(e)}")
        return False

def is_valid_species(species_id):
    return 1 <= species_id <= 386

def is_valid_level(level):
    return 1 <= level <= 100

def hex_dump(data, offset, length=32, width=16):
    """Exibe um dump hexadecimal dos dados para diagnóstico"""
    result = []
    for i in range(0, length, width):
        chunk = data[offset+i:offset+i+width]
        hex_line = ' '.join(f"{b:02X}" for b in chunk)
        ascii_line = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        result.append(f"0x{offset+i:04X}: {hex_line.ljust(width*3-1)}  {ascii_line}")
    return '\n'.join(result)

def find_pokemon_team_brute_force(data, active_block):
    """
    Busca varredura completa por estruturas que pareçam uma equipe Pokémon.
    Especificamente procura por Ivysaur ou qualquer outro Pokémon.
    """
    print("\n=== Iniciando busca intensiva por equipe Pokémon ===")
    
    block_size = 0xE000
    section_size = 0x1000
    
    # Procurar em todo o bloco ativo
    block_start = active_block * block_size
    
    # Estrutura esperada: contador de equipe (1-6) seguido por IDs de espécies válidos
    IVYSAUR_ID = 2  # Especificamente procurando por Ivysaur
    
    potential_teams = []
    
    # Vamos escanear cada seção no bloco ativo
    for section in range(14):  # Aproximadamente 14 seções em um bloco
        section_start = block_start + (section * section_size)
        
        # Escanear cada byte na seção como possível contador de equipe
        for offset in range(section_start, section_start + section_size - 20):
            party_count = data[offset]
            
            # Se parece um contador de equipe válido
            if 1 <= party_count <= 6:
                # Verificar se os próximos bytes formam IDs de espécies válidos
                # Em Fire Red, temos 4 bytes de padding após o contador, então species_offset = offset + 4
                species_offset = offset + 4
                
                # Verificar se temos pelo menos um Pokémon válido na lista
                if species_offset + 2 <= len(data):
                    try:
                        species_id = struct.unpack_from('<H', data, species_offset)[0]
                        
                        # Se encontramos um ID de espécie válido, especialmente Ivysaur
                        if is_valid_species(species_id) and (species_id == IVYSAUR_ID or True):
                            # Verificar se temos uma estrutura consistente
                            # Simular se podemos extrair dados de Pokémon desta posição
                            try:
                                team_data = extract_team_at_offset(data, party_count, species_offset, active_block, offset)
                                if team_data and team_data['team']:
                                    print(f"\nPossível equipe encontrada em 0x{offset:X}:")
                                    for pokemon in team_data['team']:
                                        print(f"  {pokemon['name']} (Nível {pokemon['level']})")
                                    
                                    potential_teams.append({
                                        'offset': offset,
                                        'team': team_data
                                    })
                            except:
                                # Se falhar, provavelmente não é uma estrutura válida
                                continue
                    except:
                        continue
    
    # Ordenar por número de Pokémon encontrados (equipes mais completas primeiro)
    potential_teams.sort(key=lambda x: len(x['team']['team']), reverse=True)
    
    if potential_teams:
        print(f"\nEncontradas {len(potential_teams)} possíveis equipes.")
        best_team = potential_teams[0]
        print(f"Usando equipe encontrada em 0x{best_team['offset']:X} com {len(best_team['team']['team'])} Pokémon.")
        return best_team['team']
    
    print("Nenhuma equipe Pokémon encontrada pela varredura completa.")
    return None

def find_pokemon_team_fire_red(data):
    """
    Tenta localizar a equipe Pokémon em um save de FireRed Rev 1 (USA/Europe)
    testando múltiplos offsets conhecidos.
    """
    # Para Fire Red, definimos os tamanhos dos blocos
    block_size = 0xE000
    section_size = 0x1000
    
    # Verificar os dois blocos de save possíveis para determinar qual está ativo
    active_block = None
    highest_save_index = -1
    
    for block_idx in range(2):
        block_start = block_idx * block_size
        # O save index está na seção 0 de cada bloco, offset 0x0FFC
        save_index_offset = block_start + 0x0FFC
        if save_index_offset + 2 <= len(data):
            save_index = struct.unpack_from('<H', data, save_index_offset)[0]
            print(f"Bloco {block_idx}: Save Index = {save_index}")
            if save_index > highest_save_index:
                highest_save_index = save_index
                active_block = block_idx
    
    if active_block is None:
        print("Não foi possível determinar o bloco de save ativo")
        return None
    
    print(f"Bloco ativo: {active_block} (Save Index: {highest_save_index})")
    
    # Offsets conhecidos para Fire Red Rev 1 (USA/Europe)
    # A equipe está na seção 1, mas o offset exato pode variar
    known_offsets = [
        0x234,    # Offset padrão documentado
        0x34,     # Offset alternativo para algumas versões
        0x238,    # Variação possível
        0x284,    # Variação regional
        0xA94,    # Outro offset relatado
        0x2F8,    # Outro offset possível
        0x34C,    # Offset adicional 1
        0x3B8,    # Offset adicional 2
        0x4A4,    # Offset adicional 3
        0x198,    # Offset adicional 4
        0x290,    # Mais possibilidades
        0x310,
        0x164,
        0x134,
        0xF34,
        0x1034
    ]
    
    for offset in known_offsets:
        section_1_start = (active_block * block_size) + section_size  # Seção 1
        party_count_offset = section_1_start + offset
        
        if party_count_offset >= len(data):
            continue
        
        party_count = data[party_count_offset]
        print(f"Testando offset 0x{offset:X}: Contador de Pokémon = {party_count}")
        
        if 1 <= party_count <= 6:
            # Parece um contador válido, vamos verificar se há dados válidos
            party_data_offset = party_count_offset + 4
            species_list_offset = party_data_offset
            
            # Verificar se temos pelo menos um Pokémon válido
            if species_list_offset + 2 <= len(data):
                try:
                    species_id = struct.unpack_from('<H', data, species_list_offset)[0]
                    if is_valid_species(species_id):
                        print(f"Encontrada equipe válida no offset 0x{offset:X}!")
                        # Continuar com este offset
                        return extract_team_at_offset(data, party_count, party_data_offset, active_block, party_count_offset)
                except:
                    continue
    
    print("Offsets conhecidos falharam. Tentando busca bruta...")
    # Se não encontramos pelos offsets conhecidos, tentar uma varredura completa
    return find_pokemon_team_brute_force(data, active_block)

def search_for_starter_pokemon(data, active_block):
    """Tenta localizar um Pokémon inicial no save"""
    print("\nProcurando por Pokémon inicial...")
    
    block_size = 0xE000
    section_size = 0x1000
    section_1_start = (active_block * block_size) + section_size
    
    # Pokémon iniciais do Fire Red: Bulbasaur (1), Charmander (4), Squirtle (7)
    starter_ids = [1, 4, 7]
    
    # Verificar várias áreas do save
    check_areas = [
        # Verificar a área de dados do PC
        {"offset": section_1_start + 0x4000, "size": 0x1000, "name": "PC Box 1"},
        {"offset": section_1_start + 0x5000, "size": 0x1000, "name": "PC Box 2"},
        # Verificar área de eventos de jogo
        {"offset": section_1_start + 0x0BE0, "size": 0x100, "name": "Área de eventos"},
    ]
    
    for area in check_areas:
        print(f"\nVerificando {area['name']}...")
        
        for i in range(0, area["size"] - 4, 4):
            offset = area["offset"] + i
            
            if offset + 4 > len(data):
                continue
                
            value = struct.unpack_from('<I', data, offset)[0]
            
            # Procurar por valores que podem ser IDs de Pokémon
            for starter_id in starter_ids:
                if value & 0xFF == starter_id:  # Verificar o byte inferior
                    print(f"Possível Pokémon inicial encontrado em 0x{offset:X}: {get_pokemon_name(starter_id)}")
                    print(f"Valor: 0x{value:08X}")
                    print(hex_dump(data, offset - 16, 64))
    
    return None

def extract_team_at_offset(data, party_count, party_data_offset, active_block, party_count_offset):
    """Extrai a equipe Pokémon a partir de um offset específico"""
    species_list_offset = party_data_offset
    pokemon_data_start = species_list_offset + (party_count * 2) + 2  # +2 para terminator
    
    team = []
    
    for i in range(party_count):
        species_id_offset = species_list_offset + (i * 2)
        
        if species_id_offset + 2 > len(data):
            print(f"Offset de species ID fora dos limites para Pokémon {i+1}")
            continue
            
        species_id = struct.unpack_from('<H', data, species_id_offset)[0]
        
        # O bloco de dados do Pokémon começa em pokemon_data_start
        pokemon_offset = pokemon_data_start + (i * 100)  # 100 bytes por Pokémon
        
        if pokemon_offset + 100 > len(data):
            print(f"Offset de dados do Pokémon fora dos limites para Pokémon {i+1}")
            continue
        
        # Extrair informações básicas para validação
        personality = struct.unpack_from('<I', data, pokemon_offset)[0]
        ot_id = struct.unpack_from('<I', data, pokemon_offset + 4)[0]
        
        # Extração do nível - está no 0x54 dentro da estrutura do Pokémon
        level_offset = pokemon_offset + 0x54
        level = data[level_offset]
        
        # Validações
        if is_valid_species(species_id) and is_valid_level(level):
            pokemon_name = get_pokemon_name(species_id)
            print(f"Pokémon {i+1}: {pokemon_name} (ID: {species_id}) - Nível {level}")
            
            team.append({
                'species_id': species_id,
                'name': pokemon_name,
                'level': level,
                'personality': personality,
                'ot_id': ot_id,
                'data_offset': pokemon_offset,
                'species_offset': species_id_offset
            })
        else:
            print(f"Dados inválidos para possível Pokémon {i+1}: Espécie={species_id}, Nível={level}")
    
    return {
        'active_block': active_block,
        'party_count_offset': party_count_offset,
        'party_count': party_count,
        'party_data_offset': party_data_offset,
        'pokemon_data_start': pokemon_data_start,
        'team': team
    }

def extract_more_pokemon_data(data, pokemon_data):
    """Extrai mais dados sobre o Pokémon com base no offset de dados já conhecido"""
    
    result = {}
    team_data = []
    
    if not pokemon_data or 'team' not in pokemon_data:
        print("Dados da equipe não encontrados")
        return None
    
    for idx, pokemon in enumerate(pokemon_data['team']):
        pokemon_offset = pokemon['data_offset']
        
        # Personality Value e OT ID
        personality = pokemon['personality']
        ot_id = pokemon['ot_id']
        
        # Extrair status e EVs
        hp_offset = pokemon_offset + 0x56
        attack_offset = pokemon_offset + 0x58
        defense_offset = pokemon_offset + 0x5A
        speed_offset = pokemon_offset + 0x5C
        sp_attack_offset = pokemon_offset + 0x5E
        sp_defense_offset = pokemon_offset + 0x60
        
        # Stats atuais
        hp = struct.unpack_from('<H', data, hp_offset)[0]
        attack = struct.unpack_from('<H', data, attack_offset)[0]
        defense = struct.unpack_from('<H', data, defense_offset)[0]
        speed = struct.unpack_from('<H', data, speed_offset)[0]
        sp_attack = struct.unpack_from('<H', data, sp_attack_offset)[0]
        sp_defense = struct.unpack_from('<H', data, sp_defense_offset)[0]
        
        # EVs e IVs ficam em outras posições, mas podemos adicionar depois
        
        # Ataques atuais
        moves_offset = pokemon_offset + 0x28
        moves = []
        pp = []
        
        for move_idx in range(4):
            move_id_offset = moves_offset + (move_idx * 2)
            pp_offset = moves_offset + 8 + move_idx
            
            move_id = struct.unpack_from('<H', data, move_id_offset)[0]
            move_pp = data[pp_offset]
            
            moves.append(move_id)
            pp.append(move_pp)
        
        pokemon_details = {
            'slot': idx + 1,
            'species_id': pokemon['species_id'],
            'name': pokemon['name'],
            'level': pokemon['level'],
            'personality': personality,
            'ot_id': ot_id,
            'stats': {
                'hp': hp,
                'attack': attack,
                'defense': defense,
                'speed': speed,
                'sp_attack': sp_attack,
                'sp_defense': sp_defense
            },
            'moves': moves,
            'pp': pp,
            'offsets': {
                'species': pokemon['species_offset'],
                'data': pokemon['data_offset'],
                'hp': hp_offset,
                'moves': moves_offset
            }
        }
        
        team_data.append(pokemon_details)
    
    result['team'] = team_data
    result['party_count_offset'] = pokemon_data['party_count_offset']
    result['party_data_offset'] = pokemon_data['party_data_offset']
    result['active_block'] = pokemon_data['active_block']
    
    return result

def read_fire_red_save(sav_file_path):
    """
    Lê e analisa um arquivo .sav do Pokemon Fire Red (USA/Europe) Rev 1,
    extraindo os dados da equipe Pokémon.
    """
    try:
        if not os.path.exists(sav_file_path):
            print(f"Arquivo não encontrado: {sav_file_path}")
            return None
            
        with open(sav_file_path, 'rb') as f:
            data = f.read()

        print(f"Tamanho do arquivo: {len(data)} bytes")
        if len(data) < 0x20000:  # 128KB
            print("Aviso: Arquivo menor que o tamanho esperado para um save de GBA")

        print("\n=== Extraindo dados da equipe Pokemon (Fire Red USA/Europe Rev 1) ===")
        pokemon_team = find_pokemon_team_fire_red(data)
        
        if pokemon_team and pokemon_team['team']:
            print("\n=== Extraindo dados adicionais da equipe ===")
            detailed_team = extract_more_pokemon_data(data, pokemon_team)
            return detailed_team
        else:
            print("Não foi possível extrair dados da equipe.")
            
            # Verificar se a ROM está no início do jogo
            print("\nVerificando se o save está no início do jogo...")
            active_block = None
            highest_save_index = -1
            
            for block_idx in range(2):
                block_start = block_idx * 0xE000
                save_index_offset = block_start + 0x0FFC
                if save_index_offset + 2 <= len(data):
                    save_index = struct.unpack_from('<H', data, save_index_offset)[0]
                    if save_index > highest_save_index:
                        highest_save_index = save_index
                        active_block = block_idx
                        
                section_1_start = block_start + 0x1000
                starter_flag_offset = section_1_start + 0xBE4  # Offset aproximado da flag de escolha do inicial
                
                if starter_flag_offset < len(data):
                    starter_flag = data[starter_flag_offset]
                    print(f"Bloco {block_idx}: Possível flag de inicial = {starter_flag}")
                    if starter_flag == 0:
                        print("É possível que o jogo esteja no início e nenhum Pokémon tenha sido obtido ainda.")
            
            # Procurar por Pokémon iniciais
            if active_block is not None:
                search_for_starter_pokemon(data, active_block)
            
            return None
        
    except Exception as e:
        print(f"Erro crítico ao processar o arquivo: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def print_pokemon_details(pokemon_data):
    """Imprime informações detalhadas sobre os Pokémon da equipe"""
    
    if not pokemon_data or 'team' not in pokemon_data:
        print("Sem dados de Pokémon para exibir")
        return
    
    print("\n===== INFORMAÇÕES DA EQUIPE POKÉMON =====")
    print(f"Offset do contador da equipe: 0x{pokemon_data['party_count_offset']:X}")
    print(f"Offset dos dados da equipe: 0x{pokemon_data['party_data_offset']:X}")
    print(f"Bloco de save ativo: {pokemon_data['active_block']}")
    print(f"Quantidade de Pokémon: {len(pokemon_data['team'])}")
    
    for pokemon in pokemon_data['team']:
        print("\n" + "=" * 40)
        print(f"SLOT {pokemon['slot']}: {pokemon['name']} (Nv. {pokemon['level']})")
        print(f"ID da espécie: {pokemon['species_id']}")
        print(f"Personality Value: 0x{pokemon['personality']:08X}")
        print(f"OT ID: 0x{pokemon['ot_id']:08X}")
        
        print("\nSTATUS:")
        print(f"HP: {pokemon['stats']['hp']}")
        print(f"Ataque: {pokemon['stats']['attack']}")
        print(f"Defesa: {pokemon['stats']['defense']}")
        print(f"Velocidade: {pokemon['stats']['speed']}")
        print(f"Ataque Especial: {pokemon['stats']['sp_attack']}")
        print(f"Defesa Especial: {pokemon['stats']['sp_defense']}")
        
        print("\nATAQUES:")
        for i, move_id in enumerate(pokemon['moves']):
            if move_id > 0:
                print(f"Ataque {i+1}: ID={move_id} (PP: {pokemon['pp'][i]})")
            else:
                print(f"Ataque {i+1}: -")
        
        print("\nOFFSETS:")
        print(f"Species ID: 0x{pokemon['offsets']['species']:X}")
        print(f"Dados completos: 0x{pokemon['offsets']['data']:X}")
        print(f"HP: 0x{pokemon['offsets']['hp']:X}")
        print(f"Ataques: 0x{pokemon['offsets']['moves']:X}")

if __name__ == '__main__':
    try:
        sav_path = 'data/Pokemon - FireRed Version (USA, Europe) (Rev 1).sav'
        
        # Permitir especificar caminho alternativo
        if len(sys.argv) > 1:
            sav_path = sys.argv[1]
            print(f"Usando arquivo de save: {sav_path}")
            
        pokemon_data = read_fire_red_save(sav_path)

        if pokemon_data:
            print_pokemon_details(pokemon_data)
        else:
            print("\nNão foi possível extrair dados da equipe Pokémon. Verifique os logs para detalhes.")
            print("\nSugestões:")
            print("1. Verifique se você já obteve algum Pokémon no jogo")
            print("2. O save pode estar no início do jogo antes de obter um Pokémon")
            print("3. Tente exportar o save novamente após avançar no jogo")
            print("4. Verifique se o caminho do arquivo está correto")
    except Exception as e:
        print(f"Erro fatal no programa: {str(e)}")
        import traceback
        traceback.print_exc()