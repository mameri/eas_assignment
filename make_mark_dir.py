import sys, os

import shutil


def read_question_parts(p_file_name):

    file_name = os.path.join(os.getcwd(), p_file_name)
    file_h = open(file_name)
    lines_read = file_h.readlines()
    q_list = []	
    for q in lines_read:
        q_split = q.split(':')
        question =  q_split[0]

        parts = q_split[1].split()
    #print parts

        q_list.append([question, parts])

    file_h.close()
    return q_list

def make_mark_file(mark_file_name, student_item, submission_item, time_snap,question_list):

        file_h = open(mark_file_name, 'w')

        str_header = 'ID:{0}  A#:{1}  @{2}\n'.format(student_item, submission_item, time_snap)

        str_seprator = '*'*len(str_header) + '\n'
        #str_seprator = ''

        half_len = len(str_header) / 2

        str_half_sep = '-'* half_len + '\n'
        str_half_space = ' '*half_len
        #str_half_space = ''


        file_h.write(str_seprator)
        file_h.write(str_header)

        file_h.write(str_seprator)

        for q in question_list:
            str_q = '{2}{0}\n{1}'.format(q[0], str_seprator, str_half_space)
            file_h.write(str_q)

            if len(q[1]) == 0:
                file_h.write('0\n')


            for part in q[1]:
                str_part = '({0})\n0\n'.format(part)
                file_h.write(str_part)

            #file_h.write(str_q)

            file_h.write('\n' + str_seprator)

        str_total = 'sum = \n{0}'.format(str_seprator)
        file_h.write(str_total)
        file_h.close()



def main(p_source_dir, p_target_dir, p_q_file):

    p_source_dir = os.path.abspath(p_source_dir)
    p_target_dir = os.path.abspath(p_target_dir)


    question_list = read_question_parts(p_q_file)

    print question_list


    if not os.path.exists(p_target_dir):
        print 'creating path', p_target_dir
        os.mkdir(p_target_dir)


    student_list = [item_prop for item_prop in os.listdir(p_source_dir)
                    if os.path.isdir(os.path.join(p_source_dir, item_prop))]	

    print 'students num: ' , len(student_list)



    for student_item in student_list:
        #student_path = os.path.join(p_target_dir, student_item)
        student_source_path = os.path.join(p_source_dir, student_item)


#        print student_source_path 
        student_submission_list = [s_item for s_item in os.listdir(student_source_path) \
        if os.path.isdir(os.path.join(student_source_path, s_item))]

        #print student_item, ':',  len(student_submission_list)


        for submission_item in student_submission_list :
            submission_source = os.path.join(student_source_path, submission_item)

            time_snap_list = [s_item for s_item in os.listdir(submission_source) \
            if os.path.isdir(os.path.join(submission_source, s_item))]

               #print len(time_snap_list)
            time_snap = ''

            if len( time_snap_list) > 1 :
                time_snap = max(time_snap_list)

            elif len(time_snap_list) == 1:
                time_snap = time_snap_list[0]

            if len(time_snap) == 0:
                continue

            time_snap_dir = os.path.join(submission_source, time_snap)

            submission_file_list = [file_item for file_item in os.listdir(time_snap_dir) \
            if os.path.exists(os.path.join(time_snap_dir, file_item))]

            #print student_item, ': sub-> filenum: ' , len(submission_file_list)

            submission_name = student_item + '_' +  submission_item + '_'+  time_snap+ '_'

            if len(submission_file_list) >= 1:
                #print 'folder'
                student_folder = os.path.join( p_target_dir, submission_name +  'dir_')

                if not os.path.exists(student_folder) :
                    #print 'creating student folder {0}'.format(student_folder)
                    os.mkdir(student_folder)

                print len(submission_file_list)
                for submission_file_item in submission_file_list:
                    submission_file_name = os.path.join(time_snap_dir, submission_file_item)

                    file_in_target = os.path.join(student_folder, submission_file_item)

                    # print os.path.exists(file_in_target)
                    # print (file_in_target)
                    # print student_folder
                    # print submission_file_name

                    if not os.path.exists(file_in_target):
                        # print 'creating ' , (file_in_target)
                        shutil.copy(submission_file_name,student_folder)

                    # if file_in_target[-3:] == 'zip':
                    #     os.system('unzip {0} -d {1} '.format(file_in_target, student_folder))


                student_mark = os.path.join( student_folder, submission_name + 'mark_.txt')


                make_mark_file(student_mark, student_item, submission_item, time_snap,question_list)




#        print student_submission_list

if __name__ == '__main__':
    argv = sys.argv[1:]
    # argv


    main(argv[0], argv[1], argv[2])
