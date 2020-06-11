/**
 * Created by 10840 on 2020/4/24.
 */

function empty(value) {
    return (value==""? true:false)
}

function string_len(value, len_num) {
    if(len_num >= value.length){
        return true
    }
    return false
}