class Task:
    # Membuat task baru
    def __init__(self, tuple:()):
        
        # Set values untuk variable contoh
        self.machine_id, self.processing_time = tuple

    # Sort
    def __lt__(self, other):
        return self.processing_time < other.processing_time

    # Cetak
    def __repr__(self):
        return ('(Machine: {0}, Time: {1})'.format(self.machine_id, self.processing_time))

# Kelas ini merepresentasikan sebuah assignment
class Assignment:

    # Membuat assignment baru
    def __init__(self, job_id:int, task_id:int, start_time:int, end_time:int):

        # Set values untuk variable contoh
        self.job_id = job_id
        self.task_id = task_id
        self.start_time = start_time
        self.end_time = end_time

    # Cetak
    def __repr__(self):
        return ('(Job: {0}, Task: {1}, Start: {2}, End: {3})'.format(self.job_id, self.task_id, self.start_time, self.end_time))    

# Kelas ini merepresentasikan sebuah jadwal
class Schedule:

    # Membuat jadwal baru
    def __init__(self, jobs:[]):
        # Set values untuk variable contoh
        self.jobs = jobs
        self.tasks = {}
        for i in range(len(self.jobs)):
            for j in range(len(self.jobs[i])):
                self.tasks[(i, j)] = Task(self.jobs[i][j])          # assign mesin dan waktu kerjanya
        self.assignments = {}

    # Mendapatkan assignment selanjutnya
    def backtracking_search(self) -> bool:
        # Memilih tasks dengan waktu berakhir lebih awal
        best_task_key = None
        best_machine_id = None
        best_assignment = None
        #print(self.tasks.items())
        #print("----")
        # Looping semua tasks
        for key, task in self.tasks.items():

            # Mendapatkan variable task
            job_id, task_id = key
            machine_id = task.machine_id
            processing_time = task.processing_time

            # Cek jika task membutuhkan predecessor, temukan jika iya
            predecessor = None if task_id > 0 else Assignment(0, 0, 0, 0)
            if (task_id > 0): 

                # Looping assignments
                for machine, machine_tasks in self.assignments.items():
                    # Break looping jika predecessor sudah ditemukan
                    if(predecessor != None):
                        break

                    # Looping tasks mesin
                    for t in machine_tasks:
                        # Cek jika ada predecessor
                        if(t.job_id == job_id and t.task_id == (task_id - 1)):
                            predecessor = t
                            break
            # Lanjutkan jika task membutuhkan predecessor dan jika tidak bisa ditemukan
            if(predecessor == None):
                continue

            # Mendapatkan assignment
            assignment = self.assignments.get(machine_id)

            # Menghitung waktu akhir
            end_time = processing_time
            if(assignment != None):
                end_time += max(predecessor.end_time, assignment[-1].end_time)
            else:
                end_time += predecessor.end_time

            # Cek apakah assignment terbaik perlu di update
            if(best_assignment == None or end_time < best_assignment.end_time):
                best_task_key = key
                best_machine_id = machine_id
                best_assignment = Assignment(job_id, task_id, end_time - processing_time, end_time)

        # Return false jika assignment tidak bisa ditemukan (masalah tidak bisa diselesaikan)
        if(best_assignment == None):
            return False

        # Tambahkan assignment terbaik
        assignment = self.assignments.get(best_machine_id)
        if(assignment == None):
            self.assignments[best_machine_id] = [best_assignment]
        else:
            assignment.append(best_assignment)

        # Hapus task
        del self.tasks[best_task_key]
        # Cek apakah sudah selesai
        if(len(self.tasks) <= 0):
            return True

        # Backtrack
        self.backtracking_search()
        
# Titik masuk utama untuk modul ini

def main():

    # baca input: banyak pekerja, banyak mesin, kumpulan waktu, kumpulan mesin
    inp = list(map(int,input().split()))
    pekerja = inp[0]
    mesinDipakai = inp[1]
    iWaktu = 2
    iMesin = 2+pekerja*mesinDipakai

    # memasukkan input ke list jobs
    jobs = []
    for i in range(pekerja):
        jobs.append([])
        for j in range(mesinDipakai):
            iTask = i*mesinDipakai+j
            jobs[i].append((inp[iMesin+iTask], inp[iWaktu+iTask]))

    # Buat jadwal
    schedule = Schedule(jobs)

    # Temukan solusi
    print(schedule.backtracking_search())

    # Cetak solusi
    print('Final solution:')
    for key, value in sorted(schedule.assignments.items()):
        print(key, value)
    print()
    
# Perintah kepada python untuk melakukan run method utama
if __name__ == "__main__": main()

"""
input:
15 15 94 66 10 53 26 15 65 82 10 27 93 92 96 70 83 74 31 88 51 57 78  8  7 91 79 18 51 18 99 33  4 82 40 86 50 54 21  6 54 68 82 20 39 35 68 73 23 30 30 53 94 58 93 32 91 30 56 27 92  9 78 23 21 60 36 29 95 99 79 76 93 42 52 42 96 29 61 88 70 16 31 65 83 78 26 50 87 62 14 30 18 75 20  4 91 68 19 54 85 73 43 24 37 87 66 32 52  9 49 61 35 99 62  6 62  7 80  3 57  7 85 30 96 91 13 87 82 83 78 56 85  8 66 88 15  5 59 30 60 41 17 66 89 78 88 69 45 82  6 13 90 27  1  8 91 80 89 49 32 28 90 93  6 35 73 47 43 75  8 51  3 84 34 28 60 69 45 67 58 87 65 62 97 20 31 33 33 77 50 80 48 90 75 96 44 28 21 51 75 17 89 59 56 63 18 17 30 16  7 35 57 16 42 34 37 26 68 73  5  8 12 87 83 20 97  7 13  5  8  4  3 11 12  9 15 10 14  6  1  2  5  6  8 15 14  9 12 10  7 11  1  4 13  2  3  2  9 10 13  7 12 14  6  1  3  8 11  5  4 15  6  3 10  7 11  1 14  5  8 15 12  9 13  2  4  8  9  7 11  5 10  3 15 13  6  2 14 12  1  4  6  4 13 14 12  5 15  8  3  2 11  1 10  7  9 13  4  8  9 15  7  2 12  5  6  3 11  1 14 10 12  6  1  8 13 14 15  2  3  9  5  4 10  7 11 11 12  7 15  1  2  3  6 13  5  9  8 10 14  4  7 12 10  3  9  1 14  4 11  8  2 13 15  5  6  5  8 14  1  6 13  7  9 15 11  4  2 12 10  3  3 15  1 13  7 11  8  6  9 10 14  2  4 12  5  6  9 11  3  4  7 10  1 14  5  2 12 13  8 15  9 15  5 14  6  7 10  2 13  8 12 11  4  3  1 11  9 13  7  5  2 14 15 12  1  8  4  3 10  6

"""
