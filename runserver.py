u"""메인 파일이지만 예제 자체는 오래됨."""
# -*- coding:utf-8 -*-
import sys

from photolog import create_app

reload(sys)
sys.setdefaultencoding('utf-8')

application = create_app()

if __name__ == "__main__":
    print "start test server..."
    application.run(host='0.0.0.0', port=5000, debug=True)
