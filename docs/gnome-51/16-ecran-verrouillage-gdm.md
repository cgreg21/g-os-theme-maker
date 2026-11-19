# Écran de verrouillage, déverrouillage et connexion GDM

Ce chapitre distingue trois interfaces qui se ressemblent mais ne fonctionnent pas dans le même contexte :

- **Écran de verrouillage** : protège une session utilisateur déjà ouverte.
- **Dialogue de déverrouillage** : demande l'authentification pour reprendre cette session.
- **Greeter GDM** : écran système affiché avant l'ouverture d'une session, pour choisir un compte et une session.

Cette distinction est indispensable pour comprendre pourquoi un thème Shell installé dans le dossier personnel ne modifie pas automatiquement l'écran de connexion.

## 1. Comprendre les trois contextes

### Écran de verrouillage

Il apparaît après Super+L, après une période d'inactivité ou lorsque le système demande le verrouillage. La session et les applications continuent d'exister. L'écran peut afficher l'heure, la date, des notifications autorisées et des informations d'état.

### Dialogue de déverrouillage

Une interaction avec l'écran verrouillé fait apparaître le dialogue d'authentification. Il appartient toujours à la session utilisateur en cours. Il ne s'agit pas du greeter GDM.

### Écran de connexion GDM

GDM est le gestionnaire de connexion. Son greeter fonctionne dans un environnement distinct de la session de bureau de l'utilisateur. Il permet de choisir un compte, une session et de s'authentifier.

GDM utilise sa propre configuration et ses propres ressources système. Le thème installé dans ~/.themes et l'extension User Themes de la session personnelle ne modifient pas automatiquement cet écran.

## 2. Repérer le contexte avant de modifier le CSS

- **Verrouillage** : session ouverte, écran verrouillé ; le style est chargé par le GNOME Shell de l'utilisateur.
- **Déverrouillage** : authentification pour reprendre la session ; le dialogue appartient au GNOME Shell de l'utilisateur.
- **Connexion GDM** : avant l'ouverture de session ; le greeter utilise son environnement et sa configuration système.

Un sélecteur CSS valide n'est utile que s'il est chargé par le bon processus Shell. Ne commencez donc jamais par copier une règle trouvée dans un thème tiers sans identifier le contexte visé.

## 3. Écran verrouillé : horloge et notifications

Dans GNOME Shell 51.0, le comportement de l'écran verrouillé est piloté par js/ui/screenShield.js. Les repères de style importants comprennent :

- .unlock-dialog-clock : groupe de l'horloge ;
- .unlock-dialog-clock-time : heure ;
- .unlock-dialog-clock-date : date ;
- .unlock-dialog-notifications-container : zone des notifications ;
- .unlock-dialog-notification-label : libellé principal ;
- .unlock-dialog-notification-count-text : résumé ou compteur ;
- #panel.lock-screen : panneau supérieur dans le contexte verrouillé.

Ces noms sont des détails d'implémentation. Vérifiez leur présence dans les sources de la version réellement utilisée.

### Exemple : améliorer la lisibilité de l'horloge

~~~css
.unlock-dialog-clock {
  color: #ffffff;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.45);
  text-align: center;
}

.unlock-dialog-clock-time {
  font-size: 64pt;
  font-weight: 700;
}

.unlock-dialog-clock-date {
  font-size: 20pt;
  font-weight: 500;
}
~~~

Les tailles sont des exemples et non les valeurs natives. Testez plusieurs résolutions et facteurs de mise à l'échelle.

### Exemple : notifications

~~~css
.unlock-dialog-notifications-container {
  spacing: 8px;
}

.unlock-dialog-notifications-container {
  spacing: 8px;
}

.unlock-dialog-notification-label {
  color: #ffffff;
}

.unlock-dialog-notification-count-text {
  opacity: 0.8;
}
~~~

Ne masquez pas toutes les notifications pour obtenir un écran plus minimaliste sans examiner les préférences de confidentialité. L'utilisateur doit pouvoir contrôler les informations visibles lorsque l'appareil est verrouillé.

## 4. Dialogue de déverrouillage

Le fichier amont _login-dialog.scss contient des règles communes aux interfaces de connexion et de déverrouillage. Les classes repères comprennent :

- .login-dialog et .unlock-dialog : conteneurs des dialogues ;
- .login-dialog-banner-view et .login-dialog-banner : bannière ;
- .login-dialog-logo-bin : emplacement du logo ;
- .login-dialog-user-list et .login-dialog-user-list-item : liste des comptes lorsqu'elle est affichée ;
- .login-dialog-prompt-layout : disposition de la demande d'authentification ;
- .login-dialog-prompt-entry : champ de saisie ;
- .login-dialog-button-box et .modal-dialog-button : groupe et boutons d'action ;
- .login-dialog-message, .login-dialog-message-warning et .caps-lock-warning-label : messages et avertissements.

Le contenu visible varie selon le mode de session et l'étape d'authentification. Ne supposez pas que tous ces éléments sont présents simultanément.

### Exemple : champ et boutons

~~~css
.unlock-dialog .login-dialog-prompt-entry {
  border-radius: 10px;
  padding: 8px 12px;
}

.unlock-dialog .modal-dialog-button {
  border-radius: 999px;
  padding: 8px 18px;
}

.unlock-dialog .modal-dialog-button:default {
  background-color: #3584e4;
  color: #ffffff;
}

.unlock-dialog .modal-dialog-button:focus {
  outline: 2px solid #ffffff;
  outline-offset: 3px;
}
~~~

Ne supprimez pas l'indication de focus et ne rendez pas les boutons de validation et d'annulation indistinguables. Une interface d'authentification doit rester immédiatement compréhensible.

## 5. Pourquoi le thème utilisateur ne change pas GDM

GDM démarre le greeter dans une session distincte. Il ne lit pas automatiquement les réglages et extensions du compte de bureau.

Les personnalisations du greeter reposent généralement sur des ressources installées au niveau système et sur une configuration dconf propre à GDM. Les chemins exacts dépendent de la distribution et du paquet installé.

À retenir :

1. Un thème installé dans ~/.themes est destiné à la session utilisateur.
2. User Themes agit dans la session où l'extension est activée ; elle ne transforme pas le greeter.
3. Les fichiers système peuvent être remplacés par une mise à jour de GNOME.
4. Les réglages dconf de GDM sont distincts de ceux du compte personnel.
5. Modifier le greeter nécessite des droits administrateur et une procédure adaptée à la distribution.

Ne copiez pas aveuglément un fichier CSS dans /usr/share/gnome-shell. Identifiez d'abord le paquet propriétaire, la configuration de la distribution et la méthode prise en charge.

## 6. Fond d'écran du verrouillage

Le fond du verrouillage est distinct du fond d'écran du bureau. La clé GSettings usuelle est org.gnome.desktop.screensaver picture-uri. La variante picture-uri-dark peut être utilisée pour le mode sombre selon la version.

Lister les paramètres disponibles :

~~~bash
gsettings list-recursively org.gnome.desktop.screensaver
~~~

Lire le fond actuel :

~~~bash
gsettings get org.gnome.desktop.screensaver picture-uri
~~~

Définir un fond pour le compte courant :

~~~bash
gsettings set org.gnome.desktop.screensaver picture-uri \
  'file:///home/utilisateur/Images/fond-verrouillage.jpg'
~~~

Remplacez le chemin d'exemple par le chemin réel. Cette commande ne configure pas nécessairement le greeter GDM : celui-ci utilise sa configuration système.

Pour un poste administré, consultez le guide GNOME consacré au profil dconf de GDM. N'appliquez pas une configuration système copiée d'une autre distribution sans l'adapter.

## 7. Méthode de test sûre

1. Commencez par modifier uniquement le thème Shell de votre compte.
2. Conservez une session de travail et un terminal accessibles.
3. Verrouillez avec Super+L.
4. Vérifiez l'horloge, les notifications, le champ et les boutons.
5. Déverrouillez normalement et vérifiez le retour au bureau.
6. Testez les thèmes clair et sombre, la mise à l'échelle et le clavier.
7. N'essayez pas un thème GDM en remplaçant les fichiers système de votre poste principal.

Pour les modifications GDM, préférez une machine virtuelle ou un instantané système. Une erreur de thème du greeter peut rendre l'écran de connexion inutilisable.

## 8. Retour arrière et dépannage

### Le verrouillage est illisible

- Désactivez la dernière règle CSS ajoutée.
- Vérifiez le contraste sur le fond réellement affiché.
- Contrôlez séparément .unlock-dialog et l'écran verrouillé.
- Consultez les journaux de session avec journalctl --user -b.

### Le greeter ne change pas

C'est attendu si vous avez seulement modifié le thème personnel. Vérifiez le profil GDM et la configuration système de votre distribution.

### L'écran de connexion est cassé

Depuis une console TTY ou un accès administrateur, restaurez les fichiers natifs depuis le paquet de la distribution ou réinstallez le paquet concerné. Ne redémarrez pas GDM sans en connaître les conséquences : cela ferme les sessions graphiques actives.

### Un thème utilisateur provoque un écran vide

Désactivez le thème depuis une console ou une session de secours, puis reconnectez-vous. Conservez une copie du thème natif avant toute modification système.

## 9. Exercices

### Exercice A — horloge

Augmentez légèrement la taille de l'heure. Vérifiez que la date reste lisible et que le groupe est centré sur plusieurs résolutions.

### Exercice B — notifications

Modifiez le rayon et l'espacement. Vérifiez les textes longs et la confidentialité des informations.

### Exercice C — dialogue

Personnalisez le champ et les boutons de déverrouillage. Vérifiez le focus clavier, le bouton par défaut et l'avertissement de verrouillage majuscule.

### Exercice D — diagnostic

Comparez le verrouillage de votre session et le greeter GDM. Notez ce qui change après connexion : utilisateur, session, extensions, paramètres et thème.

## 10. Sources officielles

- [GNOME Shell 51.0 — screenShield.js](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/js/ui/screenShield.js)
- [GNOME Shell 51.0 — unlockDialog.js](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/js/ui/unlockDialog.js)
- [GNOME Shell 51.0 — loginDialog.js](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/js/gdm/loginDialog.js)
- [GNOME Shell 51.0 — _login-dialog.scss](https://gitlab.gnome.org/GNOME/gnome-shell/-/blob/51.0/data/theme/gnome-shell-sass/widgets/_login-dialog.scss)
- [GNOME Shell 51.0 — widgets SCSS](https://gitlab.gnome.org/GNOME/gnome-shell/-/tree/51.0/data/theme/gnome-shell-sass/widgets)
- [Guide administrateur GNOME — écran verrouillé](https://help.gnome.org/system-admin-guide/desktop-shield.html)
- [Aide GNOME — écran verrouillé](https://help.gnome.org/gnome-help/shell-lockscreen.html)

Les captures de l'aide GNOME sont des références visuelles du thème standard. Certaines peuvent provenir d'une version antérieure à GNOME 51 : utilisez-les pour identifier les composants, pas comme preuve de dimensions ou de sélecteurs identiques.
