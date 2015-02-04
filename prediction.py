import pandas
import numpy


def clean_data():
    df=pandas.read_csv("/home/hmisra/Downloads/train.csv")
    return df

def clean_test_data():
    df=pandas.read_csv("/home/hmisra/Downloads/test.csv")
    return df
def hypothesis(xarray,theta):
    return numpy.dot(xarray,theta)
def cost(hypo,yarray):
    return (1/2*len(yarray))*(numpy.sum(numpy.multiply(numpy.subtract([hypo],[yarray]),numpy.subtract([hypo],[yarray]))))

def predict(theta, xarray):
    return numpy.dot(xarray,theta)

def main():
    df= clean_data()
    xarray=df[['season','holiday','workingday','weather','temp','atemp','humidity','windspeed']]
    #Code to add a row at the beginning
    #xarray.loc[-1]=[1,1,1]
    #xarray.index=xarray.index+1
    #xarray=xarray.sort()
    xarray.insert(0,'X0',[1]*len(xarray))
    pxarray=clean_test_data()
    pxarray=pxarray[['season','holiday','workingday','weather','temp','atemp','humidity','windspeed']]
    pxarray.insert(0,'X0',[1]*len(pxarray))
    theta=[1]*(len(xarray.columns))
    yarray=df['count']
    #pyarray=yarray.tail(10)                                                                                                  )
    theta=[theta]
    #print cost(hypothesis(xarray,numpy.transpose(theta)), yarray)
    for i in range(1):
        costvar=cost(hypothesis(xarray,numpy.transpose(theta)), yarray)
        temp=numpy.matrix(xarray)
        theta=numpy.dot(numpy.dot(numpy.linalg.inv(numpy.dot(temp.T,temp)), temp.T),yarray)
    predictresult=predict(numpy.transpose(theta),pxarray)
    print predictresult.shape
    predictresult.to_csv("/home/hmisra/Downloads/result.csv")
    #print pyarray








if __name__=='__main__':
    main()
