import sys, os

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def read_question_parts(p_file_name):

    file_name_dir = os.path.join(os.getcwd(), p_file_name)
    file_h = open(file_name_dir)

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


def sum_student_mark_(p_source_file, p_target_file, p_question_list):

    file_h_in = open(p_source_file, 'r')

    score_lines = file_h_in.readlines()
    file_h_in.close()




    i = 0
    sum_score = 0.0
    sum_count = 0.0


    question_header = [ [question_item, str_line, score_lines.index(str_line)]\
                        for question_item in p_question_list  for str_line in score_lines \
                     if question_item[0] in str_line]



    for question_item in question_header:

        start_i = question_item[2] + 1

        q_parts = []
        if len (question_item[0]) == 2:
            q_parts = question_item[0][1]

        ##start of question
        cur_i = start_i
        while score_lines[cur_i].find('*') >= 0:
            cur_i += 1
        start_i = cur_i

        # end of question
        cur_i = start_i
        while score_lines[cur_i].find('*') < 0:
            cur_i += 1
        end_i = cur_i

        if len(q_parts) == 0:
            sum_count +=  1
            not_valid = True
            for cur_i in range(start_i, end_i):
                if len ( score_lines[cur_i].rstrip()) > 0 and isfloat (score_lines[cur_i].rstrip() ):
                    sum_score += float(score_lines[cur_i].rstrip())
                    not_valid= False
                    break

            if not_valid :
                print 'invalid data in ', score_lines[1], question_item[0]


        else:
            cur_i = start_i
            for q_part in q_parts:
                sum_count +=  1


                while score_lines[cur_i].find(q_part) < 0 and cur_i <= end_i:
                    cur_i += 1

                if score_lines[cur_i].find(q_part) < 0 :
                    print 'invalid data in ', score_lines[1], question_item[0], q_part
                    break


                while not isfloat(score_lines[cur_i].rstrip() )  and cur_i <= end_i:
                    # print score_lines[cur_i],  q_part, question_item
                    cur_i += 1

                if isfloat(score_lines[cur_i].rstrip() ):
                    # print score_lines[cur_i],  q_part, question_item
                    sum_score += float(score_lines[cur_i].rstrip())
                else:
                    print 'invalid data in ', score_lines[1], question_item[0], q_part
                    break


    file_h = open(p_target_file, 'w')
    for score_line in score_lines:
        if score_line.find('sum') >= 0:
            break
        file_h.write(score_line.replace('*', '_'))

    str_score = 'sum  = {1:3} /  {0:3}\n'.format(sum_count, sum_score)

    file_h.write(str_score)

    file_h.close()

    os.system('textutil -convert html {0} '.format(p_target_file))


    print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    return [sum_score, sum_count]




def main(p_source_dir, p_target_dir, p_q_file, p_all_mark_file):

    p_source_dir = os.path.abspath(p_source_dir)
    p_target_dir = os.path.abspath(p_target_dir)

    p_questions = 8
    question_list = read_question_parts(p_q_file)

    print question_list

    if not os.path.exists(p_target_dir):
        print 'creating path', p_target_dir
        os.mkdir(p_target_dir)



    student_list = [item_prop for item_prop in os.listdir(p_source_dir)
                    if os.path.isdir(os.path.join(p_source_dir, item_prop))]
    print len(student_list)


    # all students
    all_mark_file_name = os.path.abspath(p_all_mark_file)
    print all_mark_file_name
    file_all_h = open(all_mark_file_name, 'w')

    ## for each student
    for student_item in student_list:
        student_target_path = os.path.join(p_target_dir, student_item)
        student_source_path = os.path.join(p_source_dir, student_item)

        if not os.path.exists(student_target_path):
            os.mkdir(student_target_path)

#        print student_source_path 
        student_submission_list = [s_item for s_item in os.listdir(student_source_path) \
        if os.path.isdir(os.path.join(student_source_path, s_item))]


        for submission_item in student_submission_list :

            submission_source = os.path.join(student_source_path, submission_item)
            submission_target = os.path.join(student_target_path, submission_item)

            if not os.path.exists(submission_target):
                os.mkdir(submission_target)

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


            time_snap_source_file = os.path.join(submission_source, time_snap, 'mark.txt')

            time_snap_dir = os.path.join(submission_target, time_snap)
            if not os.path.exists(time_snap_dir):
                os.mkdir(time_snap_dir)

            mark_file_name = os.path.join(time_snap_dir, 'mark.txt')


            [student_grade, sum_count ]= sum_student_mark_(time_snap_source_file, mark_file_name, question_list)


            student_id = student_item.split('-')
            str_for_all = '{2} = {1:3} /  {0:3}\n'.format(sum_count, student_grade, student_id[0])
            file_all_h.write(str_for_all)



    file_all_h.close()



#        print student_submission_list

if __name__ == '__main__':
    argv = sys.argv[1:]

    if len(argv) < 4 :
        print 'sum_mark_dir.py  source_dir target_dir, marking_part_file, all_mark_for_teacher.txt'
        print argv

    else:
        main(argv[0], argv[1], argv[2], argv[3])
