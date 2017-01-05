from subprocess import call

with open(sunnyvale.sh", "w") as of:
    of.write("#!/bin/bash\n")
    of.write("#PBS -l nodes=1:ppn=1\n")
    of.write("#PBS -q workq\n")
    of.write("#PBS -r n\n")
    of.write("#PBS -l walltime=48:00:00\n")
    of.write("#PBS -N stability\n")
    of.write("# EVERYTHING ABOVE THIS COMMENT IS NECESSARY, SHOULD ONLY CHANGE nodes,ppn,walltime and my_job_name VALUES\n")
    of.write("cd $PBS_O_WORKDIR\n")
    of.write("module load gcc/4.9.2\n")
    of.write("source /mnt/raid-cita/dtamayo/p2/bin/activate\n")
    of.write("python run.py {0}".format(0))
    
call("chmod u=rwx sunnyvale.sh", shell=True)
call("qsub sunnyvale.sh", shell=True)
