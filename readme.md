## relBack - Oracle Backup Report 

The relBack system was developed from the need for the DBA team's verify the implementation of existing backup policies for each Oracle database serviced by the team's task was carried out previously manually accessing each base and referring to the information related to backup or through emails sent by scripts stored on each server.
The centralization of information provides a quick and efficient in verifying the execution of each backup policy scheduling and as more systems are serviced and monitored is decentralized verification is concerned more and more staff time, both in check as the maintenance of scripts.

The relBack query information stored by the RMAN catalog to be able to cross the information regarding existing policies and thereby confirm that the backup performed was completed successfully and can be used at a time of crisis a restore and recovery of a base is needed.

### Instalation

1. Prepare Apache + PHP server environment, for people who do not have a lot of experience in apache configuration as I do, I suggest create a user on OS and using the LAMP package (https://bitnami.com/stack/lamp), simple installation, fast, works very well.
     1.1. Install apache >= 2
     1.2. Install PHP >= 5.6
     1.3. Install OCI8 in PHP
4. Download project
5. Extract for path destination (relBackPath), if you used LAMP, move the project to the APPS folder and change the file conf / httpd-prefix.conf, updating the folder path.
6. Configure CRON for schedules of project, this line is for the project to execute the routines with cron.
     ex: * * * * * php /relBackPath/artisan schedule:run >> /dev/null 2>&1
7. Edit file of configurations ".env"
     Basically base connection settings and for sending mail.
       ex: /relBackPath/.env
8. Execute script to create schema relback, preferably with user with dba permission
   ex: /relBackPath/database/script_create_relback.sql
     This script do:
         Create tablespace for relback, is necessary alter location of datafile.
         Create User relback;
         Grant permissons to relback;
         Grant Select permision on RMAN views;
         Create Tables;
         Create Views;
         Create Procedure;
         
9. In this step, when you start and configure apache, you should already be able to open the project.
     9.1. If the project start page opened normally, okay pass on.
     9.2. Review the apache configuration from the previous steps.
10. Start by registering the necessary information, in this order Client> Host> Database> Backup Policies;
11. After adding some policies, it is necessary to update the schedule, which by default is set to update the hours 00h, 06h, 12h and 18h (format HH24).
To update the schedule manually execute a procedure on the base:
execute RELBACK.SP_CREATE_SCHEDULE (sysdate-7);
By default I chose to set up the calendar with information for the last 7 days.
12. Like any good manual, if everything works out you can access the report by crossing the information between the policy agenda and the executions you perform on the Report screen.

### License

The Laravel framework is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)
