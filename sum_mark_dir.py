import sys, os

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

def main(p_source_dir, p_target_dir, p_q_file, p_all_mark_file):

    p_source_dir = os.path.abspath(p_source_dir)
    p_target_dir = os.path.abspath(p_target_dir)

    p_questions = 8
    question_list = read_question_parts(p_q_file)

    #print question_list

    if not os.path.exists(p_target_dir):
        print 'creating path', p_target_dir
        os.mkdir(p_target_dir)



    student_list = [item_prop for item_prop in os.listdir(p_source_dir)
                    if os.path.isdir(os.path.join(p_source_dir, item_prop))]
    #print student_list
    all_mark_file_name = os.path.abspath(p_all_mark_file)
    print all_mark_file_name
    file_all_h = open(all_mark_file_name, 'w')

    for student_item in student_list:
        student_path = os.path.join(p_target_dir, student_item)
        student_source_path = os.path.join(p_source_dir, student_item)

        if not os.path.exists(student_path):

            os.mkdir(student_path)

#        print student_source_path 
        student_submission_list = [s_item for s_item in os.listdir(student_source_path) \
        if os.path.isdir(os.path.join(student_source_path, s_item))]


        for submission_item in student_submission_list :
            submission_source = os.path.join(student_source_path, submission_item)

            submission_target = os.path.join(student_path, submission_item)

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

            file_h_in = open(time_snap_source_file, 'r')

            score_lines = file_h_in.readlines()
            file_h_in.close()

            time_snap_dir = os.path.join(submission_target, time_snap)

            if not os.path.exists(time_snap_dir):
                os.mkdir(time_snap_dir)

            mark_file_name = os.path.join(time_snap_dir, 'mark.txt')

            file_h = open(mark_file_name, 'w')



            #str_header = score_lines[0:2]


            #for h_item in str_header:
            #	file_h.write(h_item)

            #str_footer = score_lines[-3:-1]

            scores_pure = score_lines[2:]

            #file_h.write(str(scores_pure))

            #str_seprator = score_lines[0]
            i = 0
            sum_score = 0
            sum_count = 0

            #print question_list

            for q in question_list:

                str_q = scores_pure[i]
                i+= 1
                while str_q.find('*') < 0:

                    str_q = scores_pure[i]
                    i += 1
                    #print scores_pure[i], 'Q0'

                #file_h.write(str_q)

                str_q = scores_pure[i]
                i+= 1
                while str_q.find(str(q[0])) < 0:

                    str_q = scores_pure[i]
                    i += 1
                    #print str_q, 'Q1'

                #file_h.write(str_q)

                str_q = scores_pure[i]
                i+= 1
                while str_q.find('*') < 0:
                    str_q = scores_pure[i]
                    i += 1
                    #print str_q, 'Q2'
                #file_h.write(str_q)


                if len(q[1]) > 0:
                    #print i, scores_pure[i]
                    for part in q[1]:

                        str_part = scores_pure[i]
                        #file_h.write(str_part)
                        i += 1

                        str_score =  scores_pure[i]
                        #print str(str_score.split())
                        sum_score += float(str_score)
                        sum_count += 1
                        #file_h.write(str_score)
                        i +=  1


                elif len(q[1]) == 0:
                    str_score =  scores_pure[i]
                    sum_score += float(str_score)
                    sum_count += 1
                    #file_h.write(str_score)
                    #print 'berf 3 ', scores_pure[i -1]

                    i +=  1
                    #print 'after 3 ', scores_pure[i]

                #str_end_q =  scores_pure[i]
                #i+= 1
                #print i, scores_pure[i]
                #file_h.write(str_end_q)


            if sum_count != 8:
                print 'invalid'


            str_total = 'sum = {1}/{0}\n'.format(sum_count, sum_score)

            for s_line in score_lines:
                if s_line.find('sum') < 0:
                    file_h.write(s_line)
                else:
                    file_h.write(str_total)

            str_correction = 'This is .docx format in case you have difficulty reading .txt\n Nothing changed.\n'
            file_h.write(str_correction)
            file_h.close()

            os.system('textutil -convert docx {0} '.format(mark_file_name))


            student_id = student_item.split('-')
            str_for_all = '{2} = {1}/{0}\n'.format(sum_count, sum_score, student_id[0])
            file_all_h.write(str_for_all)



    file_all_h.close()



#        print student_submission_list

if __name__ == '__main__':
    argv = sys.argv[1:]
    print argv

    main(argv[0], argv[1], argv[2], argv[3])
