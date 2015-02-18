import sys, os

def read_question_parts(p_file_name):
    file_h = open(p_file_name)
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

def main(p_source_dir, p_target_dir, p_q_file):

    p_source_dir = os.path.abspath(p_source_dir)
    p_target_dir = os.path.abspath(p_target_dir)
    
    p_questions = 8
    question_list = read_question_parts(p_q_file)

    print question_list

    if not os.path.exists(p_target_dir):
        print 'creating path', p_target_dir
        os.mkdir(p_target_dir)

#    return

    student_list = [item_prop for item_prop in os.listdir(p_source_dir)
                    if os.path.isdir(os.path.join(p_source_dir, item_prop))]	
    #print student_list
    
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
		#print time_snap_list
		#print 'selected latest' , time_snap
	    elif len(time_snap_list) == 1:
		time_snap = time_snap_list[0]
	
	    if len(time_snap) == 0:
		continue

	    time_snap_dir = os.path.join(submission_target, time_snap)

	    if not os.path.exists(time_snap_dir):
		os.mkdir(time_snap_dir)
		
	    mark_file_name = os.path.join(time_snap_dir, 'mark.txt')
		
	    file_h = open(mark_file_name, 'w')
	    
	    str_header = 'ID:{0}  A#:{1}  @{2}\n'.format(student_item, submission_item, time_snap)
		
	    str_seprator = '*'*len(str_header) + '\n'
	    half_len = len(str_header) / 2
	    str_half_sep = '-'* half_len + '\n'
	    str_half_space = ' '*half_len

	    file_h.write(str_seprator)
	    file_h.write(str_header)

	    file_h.write(str_seprator)

	    for q in question_list:
		str_q = '{2}{0}\n{1}'.format(q[0], str_seprator, str_half_space)
		file_h.write(str_q)	

		for part in q[1]:
		    str_part = '({0})\n\n'.format(part) 
		    file_h.write(str_part)   

		file_h.write(str_seprator)

	    #for q in range(0, p_questions):
		#str_q = 'Q{0}:\n\n{1}'.format(q+1, str_seprator)
		#file_h.write(str_q)
		
	    str_total = 'sum = \n{0}'.format(str_seprator)
	    file_h.write(str_total)
	    file_h.close()
	
#        print student_submission_list

if __name__ == '__main__':
    argv = sys.argv[1:]
    print argv

    main(argv[0], argv[1], argv[2])
