# Internal Tool Setup
This repository will host our internal open source tool setup which will contain productivity tools for text- and video chat, file storage with editing and collaboration features and more tools for internal use-cases.  
It is also used for planning and evaluating possible tools.  

**This is work in progress. Do not use it in live systems!**  
As soon as this repository contains a complete setup which is ready to be used, there will be a *release*.

## Tool Evaluation

### Text Chat
#### Requirements
- private chat
- group chat
- channels (and sub-channels?)
- send files via chat
- some kind of project context would be nice
- mobile app (?)
- guest access (?)

#### Possible open source tools
- Matrix
- Rocket Chat
- Nextcloud Talk

#### Evaluation: Matrix (with Element and Synapse) (+ Jitsi)
- [Matrix](https://matrix.org/) is a decentralized and e2e-encrypted communication platform
- [Synapse](https://github.com/matrix-org/synapse) is the reference Matrix homeserver
- [Element](https://github.com/vector-im/element-web) (formerly Riot and Vector) provides Web, iOS and Android Apps (-> user-friendly on mobile) for Matrix
- [easy to set up](https://matrix.org/blog/2020/04/06/running-your-own-secure-communication-service-with-matrix-and-jitsi/) and [well documented](https://github.com/matrix-org/synapse/blob/develop/INSTALL.md)
- **implements given jitsi server into chat window for voice and video chat**
- TURN server necessary for jitsi to connect between clients behind NAT (seems to be difficult to set up)
- project context possible via "Spaces" with channels per "Space"
- modern and fast UI with common features
- Slack, Microsoft Teams and Gitter bridges (see https://element.io/blog/microsoft-teams-and-slack-integration-using-matrix/)
- requiring getting used to: "cross-signed device verification" -> additional PIN that is used for perfect-forward secrecy and needs to be entered after login to read chats from the past

### Voice / Video Chat
#### Requirements
- calls and video calls from chat window (ideally private-, group- and channel-wise)
- stable connection, good voice quality
- if possible e2e-encrypted
- usable for meetings with people from extern (-> not just accessible from chat server)

#### Possible open source tools
- Jitsi
- Rocket Chat
- Nextcloud Talk

### File Storage with editing ("Office" and more)
#### Requirements
- stores directories and files of every file format
- differentiation between (private files,) shared files and public files (see [Access Control](#access-control--user-management))
- sharing documents with people from extern (restrict to read access?) (see [Access Control](#access-control--user-management))
- edit files from file storage in browser
- edit documents, spreadsheets and presentations (Microsoft Office and open formats)
- show pdf files (possible editing via annotations?)
- edit markdown files with preview (?)
- collaborative editing for all editable formats (if possible)
#### Possible open source tools
- Nextcloud
- OnlyOffice
- Collabora

### Access Control / User Management
#### Requirements
- one user account for all services (requiring an account)
- => wide-spread software support
- access control for file storage 
    - differentiation between (private files,) shared files and public files
    - sharing documents with people from extern (restrict to read access?)
#### Possible open source tools
- Protocols: LDAP, OAuth2 / OpenID Connect
- Keycloak

### Tasks ("Kanban") (?)
### Polls / Time coordination ("Doodle") (?)
