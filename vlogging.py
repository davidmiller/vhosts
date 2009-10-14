import logging
#  Define logging behaviour
LOG_FILENAME = '.localsite.log'
logformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter( logformat )

#    if args.debug:
console_level = logging.DEBUG
  #  else:
   #     console_level = logging.ERROR


file_handler = logging.FileHandler( LOG_FILENAME )
file_handler.setFormatter( formatter )
file_handler.setLevel( logging.ERROR )
console_handler = logging.StreamHandler()
console_handler.setFormatter( formatter )
console_handler.setLevel( console_level )


ret_logger = logging.getLogger( 'retrieve' )
ret_logger.setLevel( logging.DEBUG )
ret_logger.addHandler( file_handler )
ret_logger.addHandler( console_handler )


create_logger = logging.getLogger( 'create' )
create_logger.setLevel( logging.DEBUG )
create_logger.addHandler( file_handler )
create_logger.addHandler( console_handler )
