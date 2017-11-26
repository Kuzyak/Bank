*/5 * * * * cd /home/kuzya/TEST/newsite && /home/kuzya/test/myvenv/bin/python /home/kuzya/TEST/newsite/manage.py spider_script

MAILTO=ujpenzcontact@gmail.com
*/5 * * * * cd /home/kuzya/TEST && /home/kuzya/test/myvenv/bin/python /home/kuzya/TEST/manage.py spider_script

*/2 * * * * source /home/kuzya/test/myvenv/bin/activate && cd $HOME/kuzya/TEST && python3 spider_script.py

*/1 * * * * cd /home/kuzya/TEST && /home/kuzya/test/myvenv/bin/python3 spider_script.py
