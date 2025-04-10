import pygame 
import sys  

# Paramètres du jeu
screen_width = 360  # Largeur
screen_height = 320  # Hauteur 
background_color = (255, 255, 255)  # Couleur(blanc)

# Initialisation de Pygame
pygame.init()  # Initialisation de la bibliothèque Pygame
screen = pygame.display.set_mode((screen_width, screen_height))  # Création de la fenêtre de jeu 
pygame.display.set_caption("Pytominoes")  #titre 
clock = pygame.time.Clock()  # Création objet 'clock' pour gérer la fréquence de mise à jour du jeu

# Chargement des ressources
font = pygame.font.Font(None, 16)  # police de caractères par défaut

# Paramètres du bouton "Quitter"
quit_button_color = (200, 200, 200)  #gris clair
quit_button_hover_color = (180, 180, 180)  #gris plus foncé
quit_button_text_color = (0, 0, 0)  # noir
quit_button_height = 20
quit_button_width = 60
quit_button_rect = pygame.Rect(screen_width / 2 - quit_button_width / 2, screen_height / 2 - quit_button_height / 2-100, quit_button_width, quit_button_height)

# Paramètres du bouton "Quitter"
play_button_color = (200, 200, 200)  # gris clair
play_button_hover_color = (180, 180, 180)  # gris plus foncé
play_button_text_color = (0, 0, 0)  # noir
play_button_height = 20
play_button_width = 60
play_button_rect = pygame.Rect(screen_width / 2 - play_button_width / 2, screen_height / 2 - play_button_height / 2, play_button_width, play_button_height)

# Fonction pour dessiner le bouton
def draw_button_quit(mouse_pos):
    if quit_button_rect.collidepoint(mouse_pos):  # Si souris dessus bouton
        pygame.draw.rect(screen, quit_button_hover_color, quit_button_rect)  # couleur 'hover'
    else:
        pygame.draw.rect(screen, quit_button_color, quit_button_rect)  # couleur normale
    
    pygame.draw.rect(screen, (0, 0, 0), quit_button_rect, 1)  # contour noir autour du bouton
    
    button_text = font.render("Quit", True, quit_button_text_color)  # Créer l'objet de texte "Quit" en noir
    text_rect = button_text.get_rect(center=quit_button_rect.center)  # centrer le texte dans le bouton
    screen.blit(button_text, text_rect)  # Afficher le texte "Quit" sur le bouton

def draw_button_play(mouse_pos):
    if play_button_rect.collidepoint(mouse_pos):  # Si la souris est sur le bouton
        pygame.draw.rect(screen, play_button_hover_color, play_button_rect)  # couleur 'hover'
    else:
        pygame.draw.rect(screen, play_button_color, play_button_rect)  # couleur normale
    
    pygame.draw.rect(screen, (0, 0, 0), play_button_rect, 1)  # contour noir du bouton
    
    button_text = font.render("Play", True, play_button_text_color)  # Créer l'objet de texte "play" en noir
    text_rect = button_text.get_rect(center=play_button_rect.center)  # centrer le texte dans le bouton
    screen.blit(button_text, text_rect)  # Afficher "play" sur le bouton


# Fonction pour mettre à jour les événements
def update():
    for event in pygame.event.get():  # Parcours de tous les événements Pygame
        if event.type == pygame.QUIT:  # Si l'événement est la fermeture de la fenêtre
            pygame.quit()  # Fermer Pygame
            sys.exit()  # Quitter le programme
        if event.type == pygame.MOUSEBUTTONDOWN:  # Si un clic de souris est effectué
            if event.button == 1:  # Si c'est un clic gauche (bouton 1)
                if quit_button_rect.collidepoint(event.pos):  # Si le clic est sur le bouton "Quit"
                    pygame.quit()  # Fermer Pygame
                    sys.exit()  # Quitter le programme
                if play_button_rect.collidepoint(event.pos):
                    print("Play")



# Fonction pour dessiner les éléments à l'écran
def draw():
    screen.fill(background_color)  # fond blanc
    title_text = font.render("Phytominoes", True, (0, 0, 0))  # Titre en noir
    screen.blit(title_text, (screen_width / 2 - 35, 10))  # position titre (55, 10) 
    draw_button_quit(pygame.mouse.get_pos())  # Dessiner "Quit"
    draw_button_play(pygame.mouse.get_pos())  # Dessiner "Play"
    pygame.display.flip()  # Mettre à jour l'affichage de la fenêtre

# Boucle principale du jeu
while True:
    update()  # Mettre à jour les événements du jeu (gestion des entrées utilisateur)
    draw()  # Dessiner les éléments à l'écran
    clock.tick(30)  # 30 FPS
