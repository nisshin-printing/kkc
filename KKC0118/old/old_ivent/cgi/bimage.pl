package bimage;

#####################################################
#BooImageWorkerLibrary,v1.01 / this library is free.#
#bimage.pl (C) BooBooClub 2002                      #
#####################################################



sub getsize{
	local($file,) = @_;

	if(!-f $file){
		return ('f','ファイルが存在しません');
	}

	open (IMG,"$file");
	seek IMG,0,0;
	binmode(IMG);
	read (IMG,$img,24);

	if($img =~ /^GIF8[79]a/){
		@output = &gif_file;
	}
	elsif($img =~ /^\xFF\xD8/){
		@output = &jpeg_file;
	}
	elsif($img =~ /^\x89PNG\x0D\x0A\x1A\x0A/){
		@output = &png_file;
	}
	else{
		@output = ('f','非対応のファイル形式です');
	}
	seek IMG,0,0;
	close(IMG);
	return (@output);

	sub gif_file{
		seek IMG,6,0;
		read(IMG,$size,4);
		($w,$h) = unpack("vv",$size);
		if($w ne '' && $h ne ''){
			return('size','GIF',$w,$h);
		}
		else{
			&get_size_error;
		}
	}

	sub jpeg_file{
		seek IMG,2,0;
		$flag = 0;
		while($flag == 0){
			read(IMG,$marker,4);
			($head,$marktype,$len) = unpack("aan",$marker);
			if($head ne "\xFF"){
				$flag = -1;
			}
			elsif($marktype =~ /^\xC0|\xC1|\xC2$/){
				seek IMG,1,1;
				read(IMG,$size,4);
				($h,$w) = unpack("nn",$size);
				$flag = 1;
			}
			else{
				$skip = $len - 2;
				seek IMG,$skip,1;
			}
		}
		if($w ne '' && $h ne ''){
			return('size','JPEG',$w,$h);
		}
		else{
			&get_size_error;
		}
	}

	sub png_file{
		seek IMG,16,0;
		read(IMG,$size,8);
		($w,$h) = unpack("NN",$size);
		if($w ne '' && $h ne ''){
			return('size','PNG',$w,$h);
		}
		else{
			&get_size_error;
		}
	}

	sub get_size_error{
		return('f','サイズを正しく取得できませんでした');
	}

}

1;

