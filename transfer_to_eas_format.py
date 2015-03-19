__author__ = 'ameri'

import sys, os

import shutil



def main(p_all_in_one_dir, p_eas_format_dir):
    # print p_all_in_one_dir
    # print p_eas_format_dir

    p_source_dir = os.path.abspath(p_all_in_one_dir)
    p_target_dir = os.path.abspath(p_eas_format_dir)

    if not os.path.exists(p_source_dir):
        print 'soruce does not exist. Quit!'
        return

    if not os.path.exists(p_target_dir):
        print 'creating target path: ', p_target_dir
        os.mkdir(p_target_dir)

    student_list = [item_student for item_student in os.listdir(p_source_dir)
                    if os.path.isdir(os.path.join(p_source_dir, item_student))]

    print len(student_list)

    for student_item in student_list:
        #print student_item
        student_info = student_item.replace('_dir_', '', 1).split('_')

        #print student_info

        if len(student_info) != 5:
            print 'invalid' , student_item
            continue

        student_id = student_info[0] + '_' + student_info[1]

        student_A_num = student_info[2] + '_' +  student_info[3]

        student_time = student_info[4]

        mark_file_dir  = os.path.join(p_source_dir, student_item)
        mark_file_name = student_id + '_' +student_A_num + '_' + student_time + '_mark_.txt'

        mark_file_full_path_with_id = mark_file_dir + '/' + mark_file_name

        mark_file_full_path = mark_file_dir + '/' + 'mark.txt'

        # print mark_file_name

        if not os.path.exists(mark_file_full_path_with_id):
            print 'invalid file', mark_file_full_path_with_id
            continue

        id_dir = os.path.join( p_target_dir, student_id)
        if not os.path.exists(id_dir):
            os.mkdir(id_dir)

        A_num_dir = os.path.join( id_dir, student_A_num)
        if not os.path.exists(A_num_dir):
            os.mkdir(A_num_dir)

        time_dir = os.path.join( A_num_dir, student_time)
        if not os.path.exists(time_dir):
            os.mkdir(time_dir)

        shutil.copy(mark_file_full_path_with_id,mark_file_full_path)

        print mark_file_full_path_with_id
        print mark_file_full_path

        des_file = time_dir + '/mark.txt'
        if os.path.exists(des_file):
            os.remove(des_file)

        shutil.move(mark_file_full_path, time_dir)




















if __name__ == '__main__':
    argv = sys.argv[1:]
    # argv

    if len(argv) < 2:
        print 'param needed'
        print '-> transfer_to_eas_format.py source_dir target_dir'

    else:

        main(argv[0], argv[1])
